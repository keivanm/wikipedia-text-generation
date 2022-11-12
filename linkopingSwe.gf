

concrete linkopingSwe of linkoping =

open
  SyntaxSwe,
  (S=SyntaxSwe),
  ParadigmsSwe,
  ExtendSwe,
  (E=ExtendSwe),
  SymbolicSwe,
  Prelude

in
{
lincat
  Sentence = SyntaxSwe.Phr ;
  Adv = SyntaxSwe.Adv ;
  T = Text ;
  City = Str ;
  --Rank = Str ;
  Population = Digits ;
  N = S.N ;
  NP = S.NP;
  Full_Sentence = S.Text ;
  PN = S.PN ;
  A = S.A ;
  V = S.V ;
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
  PN_String = Str ;
  Number = Card ;
  Rank = Numeral ;
  Digits = Digits ;
  Numeral = Numeral ;


-- vi vill använda två Ord tillsammans, t.ex. "femte" och "största"
oper create_ord_A : Numeral -> A -> Ord = \num, adj ->  
    let a : Str = (mkOrd num).s ;
        b : Str = (mkOrd adj).s ;
        c : Str = a ++ b  ;
    in {s = c; lock_Ord = <>} ; 
  
oper str_PN_to_NP : Str -> NP = \city -> mkNP (mkPN city) ;
--oper name_PN_to_NP : Name -> NP = \name -> mkNP (mkPN name.s) ;
oper in_municipality : Str -> N -> PN = \municipality,municipality_N -> mkPN (municipality ++ municipality_N.co)  ;

oper _of : Str -> Str -> NP = \name, ending -> mkNP (mkPN (name ++ ending)) ;
oper of_county : Str -> NP = \name -> _of name "län" ;

oper add_lang_specific : Str -> Str -> Str = \o,n -> o ++ n ;
    
oper join_phrs : Phr -> Phr -> Phr = \phr1,phr2 -> {s = phr1.s ++ "," ++ phr2.s; lock_Phr = <>};
oper join_phrs_no_comma : Phr -> Phr -> Phr = \phr1,phr2 -> {s = phr1.s ++ phr2.s; lock_Phr = <>};
oper join_phr_adv : Phr -> Adv -> Phr = \phr,adv -> {s = phr.s ++ "," ++ adv.s; lock_Phr = <>};
oper embed_phr : Phr -> Phr = \phr -> {s = embedInCommas phr.s; lock_Phr = <>};
oper add_comma_phr : Phr -> Phr = \phr -> {s = phr.s ++ bindComma; lock_Phr = <>};

oper samt_PConj : PConj = {s = "samt"; lock_PConj = <>};

oper create_municipality_NP : Str -> NP = \name -> mkNP (mkPN (name ++ "kommun")) ;
oper create_county_NP : Str -> NP = \name -> mkNP (mkPN (name ++ "län")) ;
oper create_diocese_NP : Str -> NP = \name -> mkNP (mkPN (name ++ "stift")) ;

oper create_population_NP : Str -> NP = \population -> mkNP (mkDet (mkCard (mkDigits population))) (mkN "invånare") ;



lin
    tatort_N = mkN "tätort" "tätorten" "tätorter" "tätorterna" ;
    centralort_NP = mkNP (mkN "centralort" "centralorter") ;
    residensstad_NP = mkNP (mkN "residensstad" "residensstäder") ;
    stiftstad_NP = mkNP (mkN "stiftsstad" "stiftsstäder") ; 
    kommun_N = mkN "kommun" "kommuner" ;
    lan_N = mkN "län" "län" ;
    stor_A = mkA "stor" "större" "störst" ;
    invanare_N = mkN "invånare" "invånare" ;
    gora_V = mkV "göra" "gjorde" "gjort" ;
    sverige_PN = mkPN "Sverige" ;
    ockso_Adv = mkAdv "också" ;
    date = mkAdv "1965" ;
    in_year_Prep = noPrep ;
    universitetsstad_N = mkN "universitetsstad" "universitetsstäder" ;
    grunda_V = mkV "grunda" "grundar" "grunda" "grundade" "grundat" "grundad" ;
    area_role_Prep = S.in_Prep ;
    for_diocese_Prep = S.for_Prep ;
  

    -- Örebro är en tätort vid Hjälmarens västra strand i Närke, samt centralort i Örebro kommun och residensstad i Örebro län. 
    -- Örebro är en tätort

    --Linköping är en tätort i Östergötland samt centralort i Linköpings kommun, residensstad i Östergötlands län 
    --och stiftsstad för Linköpings stift. 


    Line1_1 city city_county = mkPhr (mkCl (str_PN_to_NP city) (S.mkNP (S.mkNP S.a_Det tatort_N) (S.mkAdv area_role_Prep (create_county_NP city_county)))) ;
    Line1_2 centralort_kommun = mkNP centralort_NP (S.mkAdv area_role_Prep (create_municipality_NP centralort_kommun)) ;
    Line1_3 lan_residensstad = mkNP residensstad_NP (S.mkAdv area_role_Prep (create_county_NP lan_residensstad)) ;
    Line1_4 stiftstad = mkNP stiftstad_NP (S.mkAdv for_diocese_Prep (create_diocese_NP stiftstad)) ;
    
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
    Line2 city universities = mkPhr (mkCl (str_PN_to_NP city) (mkVP ockso_Adv (mkVP (S.mkNP (S.mkNP S.a_Det universitetsstad_N) (Line2_1 universities))))) ;
    Line2_1 universities = S.mkAdv S.with_Prep (S.mkNP S.and_Conj universities) ;
    -- (S.mkNP S.and_Conj universities)) ;
    create_university university year = 
      let university_NP : NP = symb university ;
          year_NP : NP = symb year ;
      in mkNP (mkNP university_NP (mkV2 grunda_V)) (S.mkAdv in_year_Prep year_NP) ;
      -- in mkNP (mkNP university_NP (mkV2 grunda_V)) (S.mkAdv in_year_Prep year_NP);
    
    create_universities_list university1 university2 = S.mkListNP university1 university2 ;
    add_university universityS list = mkListNP universityS list ;

    Line2_one city university = mkPhr (mkCl (str_PN_to_NP city) (mkVP ockso_Adv (mkVP (S.mkNP (S.mkNP S.a_Det universitetsstad_N) (Line2_1_one university))))) ;
    Line2_1_one university = S.mkAdv S.with_Prep university ;

    
    --Line1_utan_residensstad city centralort_kommun lan_residensstad stiftstad = join_phrs_no_comma (join_phrs_no_comma (Line1_1 city) 
    --(embed_phr (mkPhr samt_PConj (mkUtt (Line1_2 centralort_kommun))))) (mkPhr (mkUtt (mkNP S.and_Conj (Line1_3 lan_residensstad) (Line1_4 stiftstad))));
    --Line1_utan_residensstad city centralort_kommun stiftstad = join_phrs_no_comma (join_phrs_no_comma (Line1_1 city) 
    --(embed_phr (mkPhr samt_PConj (mkUtt (Line1_2 centralort_kommun))))) (mkPhr (mkUtt (mkNP S.and_Conj (Line1_3 lan_residensstad) (Line1_4 stiftstad))));

    --Line1_2 city centralort_kommun lan_residensstad stiftstad =  join_phrs_no_comma (embed_phr (mkPhr (samt_PConj) (mkUtt (Line1_2_1 city centralort_kommun)))) (mkPhr (mkUtt (mkNP S.and_Conj (Line1_2_2 city lan_residensstad) (Line1_2_3 city stiftstad))));
    --Line1_2_1 city centralort_kommun = mkNP (mkNP centralort_N) (S.mkAdv S.in_Prep (str_PN_to_NP centralort_kommun)) ;
    --Line1_2_2 city lan_residensstad = mkNP (mkNP residensstad_N) (S.mkAdv S.in_Prep (str_PN_to_NP lan_residensstad)) ;
    --Line1_2_3 city stiftstad = mkNP (mkNP stiftstad_N) (S.mkAdv S.for_Prep (str_PN_to_NP stiftstad)) ;
    --Line1 city centralort_kommun lan_residensstad stiftstad = join_phrs_no_comma (Line1_1 city) (Line1_2 city centralort_kommun lan_residensstad stiftstad);

    --Line1_2_utan_residensstad city centralort_kommun =  mkPhr (S.mkPConj S.and_Conj) (mkUtt (Line1_2_1 city centralort_kommun)) ;
    --Line1_utan_residensstad city centralort_kommun = join_phrs (Line1_1 city) (Line1_2_utan_residensstad city centralort_kommun);

    --Line2_1= (mkPhr (mkCl (str_PN_to_NP "Örebro")(SyntaxSwe.mkNP (SyntaxSwe.mkDet (GenNP (mkNP sverige_PN)) (create_ord_A (mkNumeral "9") stor_A)) tatort_N ))) ;
    
    --Örebro är Sveriges sjunde största tätort med 126 009 invånare i tätorten, och kommunen har 156 987 invånare.
    --svergies_n_storsta_tatort rank = SyntaxSwe.mkNP (SyntaxSwe.mkDet (GenNP (mkNP sverige_PN)) (create_ord_A (mkNumeral "9") stor_A)) tatort_N ;
    --svergies_storsta_tatort = SyntaxSwe.mkNP (SyntaxSwe.mkDet (GenNP (mkNP sverige_PN)) (mkOrd stor_A)) tatort_N ;
    --med_invanare = S.mkAdv S.with_Prep (mkNP (mkNP (mkDigits "7") invanare_N) (S.mkAdv S.in_Prep (mkNP S.the_Det tatort_N))) ;
    --Line2_1 city rank = mkPhr (mkCl (str_PN_to_NP city) (mkNP (svergies_n_storsta_tatort rank) med_invanare)) ;

    --mkPhr (mkCl he_NP have_V2 (mkNP it_Pron))
    --Line2_2  = embed_phr (mkPhr (S.mkPConj S.and_Conj) (mkUtt (mkCl (mkNP S.the_Det kommun_N) S.have_V2 (mkNP (mkDigits "5") invanare_N)))) ;
    --Line2 city rank = join_phrs_no_comma (Line2_1 city rank) Line2_2 ;

    --Line2_1_storsta city = mkPhr (mkCl (str_PN_to_NP city) (mkNP svergies_storsta_tatort med_invanare)) ;
   -- Line2_storsta city = join_phrs_no_comma (Line2_1_storsta city) Line2_2 ;


    --Linköping är Sveriges åttonde största tätort med över 115 000 invånare.
    Line3 city rank population = mkPhr (mkCl (str_PN_to_NP city) (S.mkNP (S.mkNP (mkDet (GenNP (mkNP sverige_PN)) (mkOrd rank))(mkCN (mkAP (mkOrd stor_A)) tatort_N))
                                  (S.mkAdv S.with_Prep (S.mkNP (mkCard (mkAdN S.more_CAdv) (mkCard population)) invanare_N))));
    
    Line3_largest city population = mkPhr (mkCl (str_PN_to_NP city) (S.mkNP (S.mkNP (mkDet (GenNP (mkNP sverige_PN)) (mkOrd stor_A)) tatort_N)
                                    (S.mkAdv S.with_Prep (S.mkNP (mkCard (mkAdN S.more_CAdv) (mkCard population)) invanare_N))));

    Line3_norank city population = mkPhr (mkCl (mkNP (mkNP (mkCard (mkAdN S.more_CAdv) (mkCard population)) invanare_N) (S.mkAdv S.in_Prep (str_PN_to_NP city)))) ;
    --Line3_norank city population = mkPhr (mkUtt (mkNP population invanare_N)) ;
    --Line3 city = mkPhr (mkCl (S.mkNP S.the_Det) (mkV3 (mkV "göra" "gjorde" "gjort") S.to_Prep) (S.mkNP (in_municipality city kommun_N)) (S.mkNP (S.mkDet (GenNP (S.mkNP sverige_PN)) (S.mkOrd stor_A)) kommun_N)) ;

    Final sentence1 sentence2 sentence3 = mkText sentence1 (mkText sentence2 (mkText sentence3)) ;
    Final_without_line2 sentence1 sentence3 = mkText sentence1 (mkText sentence3) ;

    --Final_utan_residensstad city centralort_kommun = mkText (Line1_utan_residensstad city centralort_kommun) (mkText (Line2 city) (mkText (Line3 city))) ;



    NameObject str = str.s ;
    NameObject_vowel str = str.s ;
    NameObject_consonant str = str.s ++ BIND ++ "s" ;

    pn_masc str = str ;
    pn_fem str = str ;

    UniversityObject str = str.s ;
    YearObject str = str.s ;
    CityObject str = str.s ;
    --RankObject str = str.s ;
    --PopulationObject str = str.s ; 

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
    

    --IntNumber int = <symb int : Card> ;
    --NumeralNumber numeral = mkCard numeral ;
  
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
