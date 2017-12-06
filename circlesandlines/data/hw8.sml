
(* EXERCISE 1 // binary search trees *)

datatype bstree = Lf | Br of int * bstree * bstree

fun contains x Lf = false
  | contains x (Br(k,l,r)) =
	if x=k then true
	else if x < k then contains x l
		      else contains x r

fun withalso x Lf = (Br(x,Lf,Lf))
  | withalso x (Br(k,l,r)) =
	if x=k then (Br(k,l,r))
	else if x < k then (Br(k,withalso x l,r))
		      else (Br(k,l,withalso x r))

datatype dir = Left | Right

(* path *)
local
   fun helper n Lf ds = ds
     | helper n (Br(k,l,r)) ds =
	if n=k then ds
	else if n < k then (helper n l (Left::ds))
	else (helper n r (Right::ds))
in fun path n bstree = rev(helper n bstree nil)
end

(* without *)
local
   fun min (Br(k,Lf,r)) = k
     | min (Br(k,l,r)) = min l
in fun without n Lf = Lf
     | without n (Br(k,l,Lf)) =
	if n=k then l
	else Br(k,l,Lf)
     | without n (Br(k,l,r)) =
	if n=k then let val m = (min r) in (Br(m,l,without m r)) end
	else if n<k then Br(k,without n l,r)
		    else Br(k,l,without n r)
end

(* flatten *)
local
   fun fhelp ks (Br(k,Lf,Lf)) = k::ks
     | fhelp ks (Br(k,l,Lf)) = fhelp (k::ks) l
     | fhelp ks (Br(k,Lf,r)) = k::(fhelp ks r)
     | fhelp ks (Br(k,l,r)) =
	let val ls = fhelp ks l
	    val rs = fhelp ks r
	in ls@(k::rs)
	end
in fun flatten bstree = fhelp nil bstree
end

(* EXERCISE 2 // boolean formulae *)

datatype logic = AND of logic * logic
	       | OR of logic * logic
	       | NOT of logic
	       | CONST of bool
	       | VAR of string

(* check *)
local
   fun findval s ((name, aval)::asgn) =
	(* Recursively loops through list asgn of variable+value tuples until it finds the tuple that matches the given variable name
	and returns its assigned value *)
	if s=name then aval
	else findval s asgn
   fun logparse (AND (l,r)) lval rval =
	(* Evaluates conjunctions *)
	if lval andalso rval then true
	else false
     | logparse (OR (l,r)) lval rval =
	(* Evaluates disjunctions *)
	if lval then true
	else if rval then true
	else false
in fun check (AND (l,r)) asgn =
	let val lval = check l asgn
	    val rval = check r asgn
	in
	    logparse (AND (l,r)) lval rval
	end
     | check (OR (l,r)) asgn =
        let val lval = check l asgn
            val rval = check r asgn
        in
            logparse (OR (l,r)) lval rval
        end
     | check (NOT f) asgn =
	let val fval = check f asgn
	in
	    if fval then false
	    else true
	end
     | check (CONST v) asgn =
	if v then true
	else false
     | check (VAR x) asgn = findval x asgn 
end

(* vars *)
local
   fun notinList v vs =
	if vs=nil then true
	else if v=hd(vs) then false
	else notinList v (tl(vs))
   fun addVar vs1 vs2 =
	if vs1=nil then vs2
	else if (notinList (hd(vs1)) vs2) then addVar (tl(vs1)) (hd(vs1)::vs2)
        else addVar (tl(vs1)) vs2
   fun vhelp (VAR v) vs = v::vs
     | vhelp (AND (l,r)) vs = 
	let val ls = (vhelp l vs)
	    val rs = (vhelp r vs)
	in addVar (ls@rs) vs
	end
     | vhelp (OR (l,r)) vs =
	let val ls = (vhelp l vs)
            val rs = (vhelp r vs)
        in addVar (ls@rs) vs
        end
     | vhelp (NOT f) vs = vhelp f vs
     | vhelp (CONST b) vs = nil
in fun vars logic = rev(vhelp logic nil)
end

(* tt *)

local
   fun addCol b nil [[]] = [[b]]
     | addCol b nbs [[]] = nbs
     | addCol b nbs (ob::nil) = (b::ob)::nbs
     | addCol b nbs (ob::obs) = addCol b ((b::ob)::nbs) obs
in
   fun ttrows vs =
	if vs=nil then [[]]
	else
	   let val bs = ttrows (tl vs)
	   in
	       (addCol true nil bs)@(addCol false nil bs)
	   end
end

local
   fun rowAsgn nil nil asgn = asgn
     | rowAsgn vs bs asgn = rowAsgn (tl vs) (tl bs) (((hd vs), (hd bs))::asgn)
   fun eval logic vs nil es = es
     | eval logic vs bs es = eval logic vs (tl bs) ((check logic (rowAsgn vs (hd bs) nil))::es)
   fun zip nil nil = nil
     | zip (x::xs) (y::ys) = (x,y)::(zip xs ys)
in
   fun tt logic = 
     let val vs = vars logic
	 val bs = ttrows vs
	 val es = rev(eval logic vs bs nil)
     in
	 (vs, zip bs es)
     end
end
