// MATH 221 Spring 2016
//
// Homework 10 Sample code
//
// Rewrite of my solution to Homework 9 Exercise 2.
//
// This is a modification of my BlackJack solution from 
// the last homework assignment.  It plays a one-player 
// game of BlackJack against a computer dealer.  I've 
// modified it so that it uses Go structs to represent 
// three data object types:
//
//    card - one of 52 playing cards
//    deck - a permutation of 52 playing cards
//    hand - a collection of 0 or more playing cards
//           with some hidden, the others revealed.
// 

package main

import (
	"fmt"
	"math/rand"
	"strconv"
	"time"
)

// BACKGROUND_IS_BRIGHT : bool
//
// This flag should be true if the Terminal background
// is bright; false if it is dark.
//
var BACKGROUND_IS_BRIGHT bool = false

type card struct {
    rank string
    suit string
    code int
}

type deck struct {
	top int
	cards []card
}

type hand struct {
	name string
	visible []card
	hidden  []card
}

// rank : int -> string
//
// Converts a card code (0-51) into it's rank,
// a string that is A, 2, etc., 10, J, Q, K.
//
// See makeDeck below for details.
//
func rankOf(i int) string {
	var face = map[int]string{
		1:  "A",
		11: "J",
		12: "Q",
		13: "K",
	}
	var r int = i%13 + 1
	if r >= 2 && r <= 10 {
		return strconv.Itoa(r)
	} else {
		return face[r]
	}
}

// suitOf : int -> string
//
// Converts a card code (0-51) into it's suit,
// a unicode character for spades, clubs, hearts,
// or diamonds.
//
// See https://en.wikipedia.org/wiki/
//             Playing_cards_in_Unicode
//
// See makeDeck below for details.
//
func suitOf(i int) string {

	var suits map[int]string

	if BACKGROUND_IS_BRIGHT {
		suits = map[int]string{
			0: "\u2660", // spades
			1: "\u2663", // clubs
			2: "\u2661", // hearts
			3: "\u2662", // diamonds
		}
	} else {
		suits = map[int]string{
			0: "\u2664", // spades
			1: "\u2667", // clubs
			2: "\u2665", // hearts
			3: "\u2666", // diamonds
		}
	}
	return suits[i % 4]
}

// makeCard : int -> string
//
// Given a playing card's code (0-51), returns the
// card struct corresponding to it.
// 
// The cards are coded from 0 to 12 as Ace through 
// King.  Then each suit has a range of 13 within
// the codes from 0 to 51 as follows:
//
//    0-12  spades
//    13-25 clubs
//    26-38 hearts
//    39-51 diamonds
// 
func makeCard(i int) card {
	return card{code:i, rank:rankOf(i), suit:suitOf(i)}
}


// card.value : . -> int
//
// Evaluates the card with a score from 1 to 10.
// An Ace is valued at 1.
//
func (c card) value() int {
	var r int = (c.code % 13) + 1
	if r < 10 {
		return r
	} else {
		return 10
	}
}

// toString : card -> string
//
// Returns a string representing the given card.
//
func toString(c card) string {
	return (c.rank + c.suit)
}

// makeDeck: . -> deck
//
// Makes a deck of cards, unshuffled in code order.
//
func makeDeck() deck {
	var d deck = deck{top:0, cards:make([]card, 52)}
	for position, _ := range d.cards {
		d.cards[position] = makeCard(position)
	}
	return d
}

// deck.shuffle: . -> .
//
// Shuffles a 52 card deck, randomly permuting it
// with a Knuth shuffle.
//
func (d *deck) shuffle() {
	//
	// Initialize the random number generator for shuffling.
	rand.Seed(time.Now().UnixNano())

	// Apply a Knuth shuffle.
	d.top = 0
	for position, _ := range d.cards {
		var swapWith int = rand.Intn(52 - position)
		if swapWith != position {
			d.cards[position], d.cards[swapWith] = d.cards[swapWith], d.cards[position]
		}
		position = position + 1
	}
}

// deck.dealUp: *hand -> .
//
// Takes a card from the deck and adds it, face up, to
// the given hand.
func (d *deck) dealUp(h *hand) {
	var c card = d.cards[d.top]
	d.top ++
	h.visible = append(h.visible,c)
}

// deck.dealDown: *hand -> .
//
// Takes a card from the deck and adds it, face down, to
// the given hand.
func (d *deck) dealDown(h *hand) {
	var c card = d.cards[d.top]
	d.top ++
	h.hidden = append(h.hidden,c)
}

func makeHand(s string) hand {
	return hand{name:s, visible:make([]card,0), hidden:make([]card,0)}
}

// hand.tally : . -> int
//
// Evaluates an array of playing cards as a hand
// according to BlackJack scoring.  Aces are worth
// 11 unless that makes the hand go over 21, in
// which case they can count as 1 instead.
//
func (h hand) tally() int {
	var hasAces bool = false // Keep track of whet
	var total int = 0
	for _, c := range append(h.visible,h.hidden...) {
		if c.rank == "A" {
			hasAces = true
		}
		total = total + c.value()
	}
	if hasAces && total <= 11 {
		total = total + 10
	}
	return total
}

// hand.report : . -> .
//
// Given a player name, their hand of cards, and
// a "show" flag, reports that player's hand to
// the program user.  It also reports the player's
// BlackJack tally.
//
// In some cases, a BlackJack program may not want
// to reveal the player's first card and their
// tally.  In that case, showFirst should be set
// to false.
//
func (h hand) report(show bool) {
	// Output the name.
	fmt.Print(h.name + ": \t")

	// Output the tally.
	if show || len(h.hidden) == 0 {
		fmt.Printf("WORTH: %2d\tHAND: ", h.tally())
	} else {
		// ...unless it should be hidden.
		fmt.Printf("WORTH: ??\tHAND: ")
	}

	// Output the hand of cards, perhaps hiding the
    // hidden ones.
	for _, c := range h.hidden {
		if show {
			fmt.Print(toString(c) + " ")
		} else {
			fmt.Print("?? ")
		}
	}
	for _, c := range h.visible {
		fmt.Print(toString(c) + " ")
	}
	fmt.Println()
}

// onePlay : . -> bool
//
// Determines whether the player would like to obtain
// another card, i.e., would they like to be "hit" or
// would they like to "stand"?
//
// Returns true if they want to continue play (hit to
// obtain a card), and false if they are done (want to
// stand).
//
func onePlay() bool {
	// Requests an 'H' or an 'S'.
	var s string
	fmt.Print("Would you like to hit[H]? or stand[S]? ")
	fmt.Scanln(&s)

	// Loops until the entry is correct.
	for s != "H" && s != "h" && s != "S" && s != "s" {
		fmt.Println("Please press 'H' or 'S'.")
		fmt.Print("? ")
		fmt.Scanln(&s)
	}

	// Return true if they want another card (a hit).
	return (s == "H" || s == "h")
}

// main
//
// This plays a game of one-player BlackJack using one
// shuffled deck of cards from a standard 52 card deck.
//
// After the first four cards are dealt, two to the
// dealer and two to the player, players choose to
// obtain more cards (get "hit") until they go over
// 21 (a "bust") or are satisfied with their hand.
//
// The player goes first.  The dealer then plays a
// fixed strategy to try to obtain a hand over 16.
//
// The dealer concedes, does not hit, when the player
// wins right away with 21.
//
func main() {

	//
	// Set up the deck and the two players' hands.
	var cards deck = makeDeck()
	(&cards).shuffle()
	var dealer hand = makeHand("house")
	var player hand = makeHand("you")

	//
	// Deal the first two cards of each hand.
	(&cards).dealDown(&dealer)
	(&cards).dealDown(&player)
	(&cards).dealUp(&dealer)
	(&cards).dealUp(&player)
	player.report(true)
	dealer.report(false)
	fmt.Println()

	//
	// Perform the game play of the player.
	for player.tally() < 21 && onePlay() {
		(&cards).dealUp(&player)
		player.report(true)
		dealer.report(false)
		fmt.Println()
	}
	var playerTotal int = player.tally()

	//
	// Maybe engage in dealer play.
	if playerTotal < 21 {

		//
		// The dealer follows a fixed strategy to try
		// and beat the player's score.
		fmt.Println("Okay! You've held.")
		time.Sleep(2 * time.Second)
		fmt.Println("The dealer flips his first card.")
		dealer.report(true)
		fmt.Println()
		time.Sleep(3 * time.Second)

		//
		// Keep hitting if under 17.
		for dealer.tally() < 17 {
			fmt.Println("Under 17. The dealer draws another card.\n")
			(&cards).dealUp(&dealer)
			player.report(true)
			dealer.report(true)
			time.Sleep(3 * time.Second)
			fmt.Println()
		}

	} else if playerTotal == 21 {

		//
		// The dealer is forced to stand if the player has 21.
		fmt.Println("Twenty-one!")
		time.Sleep(3 * time.Second)
		fmt.Println("The dealer reveals his hand.")
		dealer.report(true)
	}

	//
	// Report the results.
	var dealerTotal int = dealer.tally()
	if playerTotal > 21 {
		fmt.Println("BUST! I'm sorry but you lose.")
	} else if dealerTotal > 21 {
		fmt.Println("The dealer went over. You win!")
	} else if playerTotal > dealerTotal {
		fmt.Println("You win with the better total!")
	} else if playerTotal < dealerTotal {
		fmt.Println("Sorry. The dealer won.")
	} else {
		fmt.Println("No winner. A push.")
	}
}
