

concrete linkopingFre of linkoping = 

open
  SyntaxFre,
  (S=SyntaxFre),
  ParadigmsFre,
  ExtendFre,
  (E=ExtendFre),
  SymbolicFre,
  Prelude

in
{
lincat
  Sentence = SyntaxFre.Phr ;
  Adv = SyntaxFre.Adv ;
  T = Text ;
  City = Str ;
  Rank = Str ;
  population = Digits ;
  N = S.N ;
  NP = S.NP;
  Full_Sentence = S.Text ;
  PN = S.PN ;
  A = S.A ;
  V = S.V ;
  Numeral = S.Numeral ;
  Number = S.Card ;
  V = S.V ;
  S = S.S ;
  ListNP = S.ListNP ;
  Year = Str ;
  University = Str ;
  AdA = S.Adv ;
  Prep = S.Prep ;
  --Name = {s : Str} ;
  Name = Str ;
  --Name = {s : Class => Str ; o : Str} ;
  StringName = Str ;
  PN_String = S.PN ;
  Digits = Digits ;


oper str_PN_to_NP : Str -> NP = \city -> mkNP (mkPN city) ;

oper add_lang_specific : Str -> Str -> Str = \o,n -> o ++ n ;
    
oper join_phrs : Phr -> Phr -> Phr = \phr1,phr2 -> {s = phr1.s ++ "," ++ phr2.s; lock_Phr = <>};
oper join_phrs_no_comma : Phr -> Phr -> Phr = \phr1,phr2 -> {s = phr1.s ++ phr2.s; lock_Phr = <>};
oper join_phr_adv : Phr -> Adv -> Phr = \phr,adv -> {s = phr.s ++ "," ++ adv.s; lock_Phr = <>};
oper embed_phr : Phr -> Phr = \phr -> {s = embedInCommas phr.s; lock_Phr = <>};
oper add_comma_phr : Phr -> Phr = \phr -> {s = phr.s ++ bindComma; lock_Phr = <>};

oper samt_PConj : PConj = {s = "et"; lock_PConj = <>};
--oper mkYear : NP -> Adv = \year -> mkAdv (mkPrep "en") year ;
--oper get_s : Card -> String = \c -> c.s ! singular


oper create_municipality_NP : PN -> NP = \name -> mkNP S.the_Det (mkCN (mkN2 (mkN "commune") genitive) (mkNP name)) ;
oper create_county_NP : PN -> NP = \name -> mkNP S.the_Det (mkCN (mkN2 (mkN "comté") genitive) (mkNP name)) ;
oper create_diocese_NP : PN -> NP = \name -> mkNP S.the_Det (mkCN (mkN2 (mkN "évêché") genitive) (mkNP name)) ;

lin

    tatort_N = mkN "zone urbaine" ;
    centralort_NP = mkNP (mkN "siège") ;
    residensstad_NP = mkNP (mkN "chef-lieu") ;
    stiftstad_NP = mkNP (mkN "siège" feminine) ; 
    kommun_N = mkN "municipalité" ;
    lan_N = mkN "comté" ;
    stor_A = mkA "grand" ;
    invanare_N = mkN "habitant" ;
    gora_V = mkV "faire" ;
    sverige_PN = mkPN "Suède" ;
    ockso_Adv = mkAdv "aussi" ;
    date = mkAdv "1965" ;
    universitetsstad_N = mkN "ville universitaire" ;
    grunda_V = mkV "fonder" ;
    in_year_Prep = mkPrep "en" ;
    for_diocese_Prep = mkPrep "" ;

    --add_ending_municipality s = s ++ "kommun" ;
    --add_ending_county s = s ++ "län" ;
    --gora_V3 = mkV3 (mkV "göra" "gjorde" "gjort") S.to_Prep ;
    --gora_till_V3 = mkV3 (mkV "göra" "gjorde" "gjort") to_Prep ;

    -- Örebro är en tätort vid Hjälmarens västra strand i Närke, samt centralort i Örebro kommun och residensstad i Örebro län. 
    -- Örebro är en tätort

    --Linköping är en tätort i Östergötland samt centralort i Linköpings kommun, residensstad i Östergötlands län 
    --och stiftsstad för Linköpings stift. 

    
    Line1_1 city city_county  = 
      let city_NP : NP = symb city ; 
          city_county_NP : NP = create_county_NP city_county ;
      in mkPhr (mkCl city_NP (S.mkNP (S.mkNP S.a_Det tatort_N) (S.mkAdv in_Prep city_county_NP))) ;
    Line1_2 centralort_kommun = 
      let centralort_kommun_NP : NP = create_municipality_NP centralort_kommun ;
      in mkNP centralort_NP (S.mkAdv S.in_Prep centralort_kommun_NP) ;
    Line1_3 lan_residensstad = 
      let lan_residensstad_NP : NP = create_county_NP lan_residensstad ;
      in mkNP residensstad_NP (S.mkAdv S.in_Prep lan_residensstad_NP) ;
    Line1_4 stiftstad = 
      let stiftstad_diocese : NP = create_diocese_NP stiftstad ;
      in mkNP stiftstad_NP (S.mkAdv for_diocese_Prep stiftstad_diocese) ;
    
    --Line1 city city_county centralort_kommun lan_residensstad stiftstad = join_phrs_no_comma (join_phrs_no_comma (Line1_1 city city_county) 
    --(add_comma_phr (mkPhr samt_PConj (mkUtt (Line1_2 centralort_kommun))))) (mkPhr (mkUtt (mkNP S.and_Conj (Line1_3 lan_residensstad) (Line1_4 stiftstad))));
    
    Line1 city city_county list = join_phrs_no_comma (Line1_1 city city_county)
      (mkPhr samt_PConj (mkUtt (mkNP S.and_Conj list))) ;
    
    Line1_one city city_county np = join_phrs_no_comma (Line1_1 city city_county)
      (mkPhr samt_PConj (mkUtt np)) ;
    
    Line1_none city city_county = Line1_1 city city_county ;

    create_list line1 line2 = S.mkListNP line1 line2 ;
    add_line line list = mkListNP line list ;
    
    --Linköping är också en universitetsstad med Linköpings universitet grundat 1975.

    --Line2 city universities = mkPhr (mkCl (str_PN_to_NP city) (S.mkNP (S.mkNP S.a_Det universitetsstad_N) (S.mkAdv with_Prep (S.mkNP and_Conj universities)))) ;
    --Line2 city universities = mkPhr (mkCl (str_PN_to_NP city) (S.mkNP (S.mkNP S.a_Det universitetsstad_N) (Line2_1 universities))) ;
    Line2 city universities = 
      let city_NP : NP = symb city ;
      in mkPhr (mkCl city_NP (mkVP ockso_Adv (mkVP (S.mkNP (S.mkNP S.a_Det universitetsstad_N) (Line2_1 universities))))) ;
    Line2_1 universities = S.mkAdv S.with_Prep (S.mkNP S.and_Conj universities) ;
    -- (S.mkNP S.and_Conj universities)) ;
    
    create_university university year = 
      let university_NP : NP = symb university ;
          year_NP : NP = symb year ;
      in mkNP (mkNP university_NP (mkV2 grunda_V)) (S.mkAdv in_year_Prep year_NP);
    
    create_universities_list university1 university2 = S.mkListNP university1 university2 ;
    add_university universityS list = mkListNP universityS list ;

    
    Line2_one city university = 
      let city_NP : NP = symb city ;
      in mkPhr (mkCl city_NP (mkVP ockso_Adv (mkVP (S.mkNP (S.mkNP S.a_Det universitetsstad_N) (Line2_1_one university))))) ;
    Line2_1_one university = S.mkAdv S.with_Prep university ;


    --mkUtt (mkNP (mkNP man_N) (mkAdv genitive (mkNP king_N)))
    --Line3 city rank population = 
     -- let city_NP : NP = symb city ;
    --  in mkPhr (mkCl city_NP (S.mkNP (S.mkNP (S.mkDet S.the_Quant (S.mkOrd rank))(mkCN (mkAP (mkOrd stor_A)) tatort_N)) (S.mkAdv genitive (S.mkNP sverige_PN))) ) ;    

    --Line3 city = mkPhr (mkCl (S.mkNP S.the_Det) (mkV3 (mkV "göra" "gjorde" "gjort") S.to_Prep) (S.mkNP (in_municipality city kommun_N)) (S.mkNP (S.mkDet (GenNP (S.mkNP sverige_PN)) (S.mkOrd stor_A)) kommun_N)) ;
     Line3 city rank population = 
    let city_NP : NP = symb city ;
    in mkPhr (mkCl city_NP (S.mkNP (S.mkNP (S.mkNP (S.mkDet S.the_Quant (S.mkOrd rank))(mkCN (mkAP (mkOrd (prefixA stor_A))) tatort_N)) (S.mkAdv genitive (S.mkNP sverige_PN)))
                                  (S.mkAdv S.with_Prep (S.mkNP (mkCard (mkAdN S.more_CAdv) (mkCard population)) invanare_N))));
    
    Line3_largest city population = 
    let city_NP : NP = symb city ;
    in mkPhr (mkCl city_NP (S.mkNP (S.mkNP (S.mkNP (S.mkDet S.the_Quant (mkOrd (prefixA stor_A))) tatort_N) (S.mkAdv genitive (S.mkNP sverige_PN)))
                                    (S.mkAdv S.with_Prep (S.mkNP (mkCard (mkAdN S.more_CAdv) (mkCard population)) invanare_N))));

    Line3_norank city population = 
    let city_NP : NP = symb city ;
    in mkPhr (mkCl (mkNP (mkNP (mkCard (mkAdN S.more_CAdv) (mkCard population)) invanare_N) (S.mkAdv S.in_Prep city_NP))) ;  


    Final sentence1 sentence2 sentence3 = mkText sentence1 (mkText sentence2 (mkText sentence3)) ;
    Final_without_line2 sentence1 sentence3 = mkText sentence1 (mkText sentence3) ;

    --Final_utan_residensstad city centralort_kommun = mkText (Line1_utan_residensstad city centralort_kommun) (mkText (Line2 city) (mkText (Line3 city))) ;



    NameObject str = str.s ;
    NameObject_vowel str = str.s ;
    NameObject_consonant str = str.s ;

    pn_masc str = mkPN str masculine;
    pn_fem str = mkPN str feminine ;

    UniversityObject str = str.s ;
    YearObject str = str.s ;
    CityObject str = str.s ;
    RankObject str = str.s ;

    mkNumeral1 = mkNumeral "1" ;
    mkNumeral2 = mkNumeral "2" ;
    mkNumeral3 = mkNumeral "3" ;
    mkNumeral4 = mkNumeral "4" ;
    mkNumeral5 = mkNumeral "5" ;
    mkNumeral6 = mkNumeral "6" ;
    mkNumeral7 = mkNumeral "7" ;
    mkNumeral8 = mkNumeral "8" ;
    mkNumeral9 = mkNumeral "9" ;
    mkNumeral10 = mkNumeral "10" ;
    --IntNumber int = <symb int : Card> ;
    --NumeralNumber numeral = mkCard numeral ;
    
    mkDigit0 = mkDigits S.n0_Dig ;
    mkDigit1 = mkDigits S.n1_Dig ;
    mkDigit2 = mkDigits S.n2_Dig ;
    mkDigit3 = mkDigits S.n3_Dig ; 
    mkDigit4 = mkDigits S.n4_Dig ;
    mkDigit5 = mkDigits S.n5_Dig ;  
    mkDigit6 = mkDigits S.n6_Dig ;
    mkDigit7 = mkDigits S.n7_Dig ; 
    mkDigit8 = mkDigits S.n8_Dig ; 
    mkDigit9 = mkDigits S.n9_Dig ; 

    mkDigits0 digits = mkDigits S.n0_Dig digits ;  -- (mkDigits n8_Dig (mkDigits n6_Dig)) -> 86 => 0 + digits
    mkDigits1 digits = mkDigits S.n1_Dig digits ; 
    mkDigits2 digits = mkDigits S.n2_Dig digits ; 
    mkDigits3 digits = mkDigits S.n3_Dig digits ;
    mkDigits4 digits = mkDigits S.n4_Dig digits ;
    mkDigits5 digits = mkDigits S.n5_Dig digits ;
    mkDigits6 digits = mkDigits S.n6_Dig digits ;
    mkDigits7 digits = mkDigits S.n7_Dig digits ;
    mkDigits8 digits = mkDigits S.n8_Dig digits ;
    mkDigits9 digits = mkDigits S.n9_Dig digits ;

-- Goteborg är Sveriges näst största tätort, efter Stockholm, med 600000 invånare.

{--
Linköping är en tätort i Östergötland samt centralort i Linköpings kommun, residensstad i Östergötlands län och stiftsstad för Linköpings stift. 
Linköping är också en universitetsstad med Linköpings universitet grundat 1975.
Linköping är Sveriges åttonde största tätort med över 115 000 invånare.
--}

{--
Örebro är en tätort vid Hjälmarens västra strand i Närke, samt centralort i Örebro kommun och residensstad i Örebro län. 
Örebro är Sveriges sjunde största tätort med 126 009 invånare i tätorten, och kommunen har 156 987 invånare.
Det gör Örebro kommun till Sveriges sjätte största kommun.
--}


}
