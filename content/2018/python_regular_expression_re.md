# Python Regular Expression[re]

> 2018

RegularExpression

Python Regular Expression[re]

EN version

SyntaxDescriptionCharacterExpression ExampleFull Match Example General Characters     Match itselfMatches the character itselfabcabcabc .Matches any character except a newline \n. In DOTALL mode, it can also match newlines.a.ca.cabc \Escape character, makes the following character literal. Use \ to match special characters.a\.ca\.ca.c [ ... ]Character set (character class). Matches any character in the set. Can specify characters or ranges.a[bcd]ea[bcd]eabe, ace, ade  Special characters lose their meaning in character sets. Escape -, ], ^ if needed.[a-c][^abc]Any character except abc Predefined Character Sets (can also be used within [ ... ])     \dMatches a digit [0-9]a\dca\dca1c, a3c \DMatches a non-digit [^0-9]a\Dca\Dcabc, axc \sMatches a whitespace character [ \t\r\n\f\v]a\sca\sca c, a\tc \SMatches a non-whitespace character [^ \t\r\n\f\v]a\Sca\Scabc, axc \wMatches a word character [A-Za-z0-9_]a\wca\wcabc, a1c \WMatches a non-word character [^A-Za-z0-9_]a\Wca\Wca@c Quantifiers (used after a character or ( ... ))     *Matches the preceding character 0 or more timesabc*abc*ab, abc, abcc +Matches the preceding character 1 or more timesabc+abc+abc, abcc ?Matches the preceding character 0 or 1 timeabc?abc?ab, abc {m}Matches the preceding character exactly m timesab{2}cab{2}cabbc {m,n}Matches the preceding character between m and n times, inclusiveab{1,2}cab{1,2}cabc, abbc *? +? ??Makes * + ? {m,n} non-greedya.*?See examples belowNon-greedy match Boundary Matchers (do not consume characters in the string)     ^Matches the beginning of the string. In multiline mode, matches the start of each line.^abc^abcabc $Matches the end of the string. In multiline mode, matches the end of each line.abc$abc$abc \AMatches only at the start of the string\Aabc\Aabcabc \ZMatches only at the end of the stringabc\Zabc\Zabc \bMatches a word boundary\babc\b\babc\babc \BMatches a non-word boundarya\Bbca\Bbca@bc Logical and Groupi
