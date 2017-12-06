package main

// This code is a combination of the program components found at:
//
//   https://tour.golang.org/concurrency/9
//   http://schier.co/blog/2015/04/26/a-simple-web-scraper-in-go.html
//   https://golang.org/pkg/net/http/
//   https://godoc.org/golang.org/x/net/html

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
	"path"
	"os"
	"time"

	"golang.org/x/net/html"
)

// The main.
func main() {
	listener := make(chan string)	// Sends messages to output (Report <- Crawl)
	counter := make(chan int)		// Counts images downloaded (DLImage <-> DLLimiter)
	irequest := make(chan string)	// Sends image URLs (DLImage <- Crawl)
	ready := make(chan bool)		// Synchronization (DLImage <- DLLimiter)
	stop := make(chan bool)			// Signals when to stop the program (Recorder.Loop <- DLImage)
	recorder := makeRecorder()

	var max int = 30 				// Maximum number of images to be downloaded

	go DLLimiter(max, counter, ready)
	go Crawl("http://processing.org", 4, recorder, listener, irequest)
	go DLImage(irequest, counter, ready, stop)
	go Report(listener)
	recorder.Loop(stop)
}

// * * *
// Interface for recording and caching URL requests, inhabited below.
//

type Recorder interface {

	// Record checks to see if a URL has been fetched and recorded.
	// Returns nil if the URL had already been recorded.  If not, records
	// the URL and returns a pointer to a struct where the URL's page can be
	// recorded.
	//
	Record(url string) *urlResult

	// Runs the recorder.
	Loop(stop chan bool)
}

// * * *
// Crawler code, relies on Crawl and Fetch.
//

// Crawl(url, depth, recorder, reporter, irequest)
//
// Crawl recursively crawls web pages starting with a seed 'url',
// to a maximum of 'depth'.  It works with a 'recorder' to report
// each successful fetch.
//
func Crawl(page_url string, depth int, recorder Recorder, reporter chan<- string, irequest chan<- string) {

	// Have we searched too deep? If so, don't fetch this one.
	if depth <= 0 {
		// reporter <- "Stop."
		return
	}

	// Have we already fetched this URL?  Record it if we haven't.
	info := recorder.Record(page_url)
	if info == nil {
		// reporter <- "Refetch."
		return
	}

	// Okay, fetch the URL.
	text, links, imgs, success := Fetch(page_url)
	if !success {
		reporter <- fmt.Sprintf("---\nFetch of %s failed.", page_url)
		return
	}

	// Record our fetch.
	info.body = text
	info.urls = links

	// Report our fetch.
	preview := 50
	if len(text) < preview {
		preview = len(info.body)
	}
	reporter <- fmt.Sprintf("---\nFetched %s: '%q...' with %d links and %d images.",
		page_url, text[:preview], len(links), len(imgs))

	// Send request for image to be downloaded
	for _, img := range imgs {
		irequest <- img
	}

	// Recursively crawl the links found at this URL.
	for _, u := range links {
		go Crawl(u, depth-1, recorder, reporter, irequest)
	}

	return
}

// Report(reporter)
//
// Outputs messages sent from Crawl.
//
func Report(reporter <-chan string) {
	for {
		msg := <-reporter
		fmt.Println(msg)
	}
}

// text, links, err := Fetch(url)
//
// Performs a HTTP fetch of the HTML text and link URL strings
// according to a web URL string.
//
func Fetch(url string) (string, []string, []string, bool) {

	if result, err := http.Get(url); err == nil {

		// Successfully fetched.  Now parse the HTML text, extracting links.
		links := make([]string, 0)
		images := make([]string, 0)

		body := result.Body
		bytes, _ := ioutil.ReadAll(body)
		text := string(bytes)

		// Read all the contents of the fetched HTML, appending to 'links'.
		ts := html.NewTokenizer(strings.NewReader(text))
		done := false
		for !done {

			// Inspect the token type of the next HTML token.
			tt := ts.Next()
			switch tt {

			// If it is the start of an HTML tag...
			case html.StartTagToken:
				tk := ts.Token()

				// and it is a "<a ...> tag...
				if tk.Data == "a" {
					// Look for an "href=..." attribute in that tag.
					for _, a := range tk.Attr {
						if a.Key == "href" && strings.Index(a.Val, "http") == 0 {
							// Found an "href" property, it's a link!
							links = append(links, a.Val)
							break
						}
					}
				} else if tk.Data == "img" {
					// Look for a "src=..." attribute in that tag.
					for _, a := range tk.Attr {
						if a.Key == "src" {
							// Found an "src" property, it's a URL for the image.
							img_url, success := FullIMGurl(url, a.Val)
							if success {
								images = append(images, img_url)
								break
							}
						}
					}
				}

			// If instead we've hit the end of the HTML token stream.
			case html.ErrorToken:
				done = true
			}

		}

		return text, links, images, true

	} else {

		// Failed to fetch.
		return "", nil, nil, false
	}
}

// string := FullIMGurl(page_url, img)
//
// Inspects an image URL (obtained from Fetch) and attempts to build the 
// full image URL.
// Because otherwise a lot of the "downloaded images" are actually error pages.
//
func FullIMGurl(page_url string, img string) (string, bool) {
	var img_url string

	if len(img) < 4 || path.Ext(img) == "" { 
		// Just in case...because it did panic a couple of times. (Though I 
		// couldn't replicate the error again afterwards.)
		// At first I was confused, since file name+extension is already 
		// five characters minimum, but it turns out some of the fetched 'img's 
		// don't have extensions.
		return "", false
	}

	if img[:4] != "http" {
		// Image URL is not a full URL, e.g. 'example.jpg'

		if img[0] == 47 {
			// Image URL is prefixed by a forward slash, e.g. '/example.jpg'
			urlComp := strings.Split(page_url, "/")
			host_url := urlComp[0] + "//" + urlComp[2]
			if host_url[:4] != "http" {
				// Host URL doesn't have 'http' prefix (was probably 
				// in the form 'www.site.thing')
				host_url = "http:" + host_url
			}
			img_url = host_url + img

		} else if path.Ext(page_url) != "" {
			// Page URL contains a file extension, e.g. '.../example.html'
			urlComp := strings.Split(page_url, "/")
			dir_url := urlComp[0] + "//" + path.Dir(strings.Join(urlComp[2:], "/"))
			img_url = dir_url + "/" + img

		} else {
			img_url = page_url + "/" + img
		}

		return img_url, true
	}

	return img, true
}

// data, err := FetchImage(url)
//
// Performs a HTTP fetch of the web image file at the given URL.
//
func FetchImage(url string) ([]byte, bool) {

    result, errg := http.Get(url)

    if errg != nil {
        return nil, false
    }

    data, errr := ioutil.ReadAll(result.Body)

    if errr != nil {
		return nil, false
    }
	return data, true
}

// ExtractFilename(page_url)
//
// Gets the base filename of the document specified by the URL.
//
func ExtractFilename(page_url string) string {
	u,err := url.Parse(page_url)
	if err != nil {
		return ""
	} else {
		return path.Base(u.Path)
	}
}

// SaveImage(filename,data)
//
// Writes raw image 'data' to a file named by 'filename'.
//
func SaveImage(filename string, data []byte) {
	ioutil.WriteFile(filename, data, 0777)
}

// DLImage(irequest, counter, ready, stop)
// 
// Takes an incoming URL (via irequest) from Crawl and tries to download the 
// image at that URL.
// Updates the download count when successful and sends the information to 
// DLLimiter (via counter).
// Sends a signal to stop the entire program when the download limit has 
// been reached (via stop, to Recorder.Loop).
// 
func DLImage(irequest chan string, counter chan int, ready <-chan bool, stop chan<- bool) {
	var c int
	var url string

	for {
		select {
			// Waits for the "go ahead" from DLLimiter
			case <-ready:
				c = <-counter

				// Processes image download requests sent by Crawl
				url = <-irequest
				data, success := FetchImage(url)
				filename := ExtractFilename(url)
				if success {
					SaveImage(filename, data)
					fmt.Printf("Successfully downloaded %s\n", filename)
					c += 1
				} else {
					fmt.Printf("Failed to download %s at: \n%s\n", filename, url)
				}
				counter <- c

			case <-time.After(time.Second):
				stop <- true
				break
		}
	}
}

// DLLimiter(max, counter, ready)
//
// Controls how many images are downloaded by checking the count updated by 
// DLImage (via counter) and signaling whether to continue downloading (via 
// ready).
//
func DLLimiter(max int, counter chan int, ready chan<- bool) {
	var c int

	// Initialize
	ready <- true
	counter <- 0

	for {
		c = <-counter
		fmt.Printf("Downloaded %d image(s)\n", c)
		if c < max {
			ready <- true
			counter <- c
		} else {
			fmt.Println("Download limit met.")
			break
		}
	}
}

// * * *
// Recorder
//

type urlResult struct {
	body string
	urls []string
}

type recorderRequest struct {
	url   string
	reply chan (*urlResult)
}

type realRecorder struct {
	hits map[string]*urlResult
	port chan recorderRequest
}

func (r realRecorder) Record(u string) (page *urlResult) {
	ack := make(chan *urlResult)
	r.port <- recorderRequest{url: u, reply: ack}
	page = <-ack
	return
}

// Constructs a recorder interface, and spawns a
// component that handles requests from clients
// of that interface.
func makeRecorder() (recorder realRecorder) {

	// Build the recorder.
	hs := make(map[string]*urlResult)
	p := make(chan recorderRequest)
	recorder = realRecorder{hits: hs, port: p}

	return
}

func (recorder realRecorder) Loop(stop chan bool) {
	hs := recorder.hits
	p := recorder.port
	for {
		select {

			case <-stop:
				fmt.Println("Program closed. (Reached maximum for images downloaded)")
				close(p)
				os.Exit(0)

			default:
				// Get a request.
				r := <-p
				// Has r.url already been recorded?
				if _, has := hs[r.url]; has {

					// If so, acknowledge that it has.
					r.reply <- nil

				} else {

					// If not, record it and respond with a struct for the page's info.
					resultHolder := &urlResult{body: "", urls: nil}
					hs[r.url] = resultHolder
					r.reply <- resultHolder
				}
		}
	}
}
