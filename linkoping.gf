
abstract linkoping = {

cat
  Numeral ;
  Digits ;
  Full_Sentence;
  Sentence ;
  NP ;
  T ;
  Adv;
  City ;
  Rank ;
  Population ;
  Num ;
  N ;
  PN ;
  A ;
  V ;
  V3 ;
  Number ;
  ListNP ;
  S ;
  Year ; 
  University ;
  Adv ;
  Prep ;
  Name ;
  Test ;
  StringName ;
  PN_String ;
  Number ;
  
fun

    tatort_N : N ;
    centralort_NP : NP;
    residensstad_NP : NP ;
    kommun_N : N ; 
    lan_N : N ;
    stor_A : A ;
    invanare_N : N ;
    gora_V : V ;
    gora_V3 : V3 ;
    sverige_PN : PN ;
    stiftstad_NP : NP ;
    universitetsstad_N : N ;
    ockso_Adv : Adv ;
    grunda_V : V ;
    in_year_Prep : Prep ;
    of_seat_Prep : Prep ;
    area_role_Prep : Prep ;
    for_diocese_Prep : Prep ;

    --gora_till_V3: V ;

    add_ending_municipality : Name -> NP ;

    create_name_vowel : Name -> Name ;
    create_name_consonant : Name -> Name ;

    --create_municipality : String -> String ;
    --create_county : String -> String ;

    Create_Test : String -> Test ;
    TestObject : String -> Test ;

    Line1_1 : Name -> PN_String -> Sentence ;
    Line1_2 : PN_String -> NP ;
    Line1_3 : PN_String -> NP ;
    Line1_4 : PN_String -> NP ;
    --Line1 : City -> City -> City -> City -> City -> Sentence ;
    Line1 : Name -> PN_String -> ListNP -> Sentence ;
    Line1_one : Name -> PN_String -> NP -> Sentence ;
    Line1_none : Name -> PN_String -> Sentence ;

    create_list : NP -> NP -> ListNP ;
    add_line : NP -> ListNP -> ListNP ;

    --Line1_2_utan_residensstad : City -> City -> Sentence ;
    --Line1_utan_residensstad : City -> City -> Sentence ;

    --svergies_n_storsta_tatort : Rank -> NP ;
    --svergies_storsta_tatort : NP ;
    --med_invanare : Adv ;

    --Line2_1 : City -> Rank -> Sentence ;
    --Line2_2 : Sentence ;
    --Line2 : City -> Rank -> Sentence ;

    --Line2_1_storsta : City -> Sentence ;
    --Line2_storsta : City ->Sentence ;

    Line2 : Name -> ListNP -> Sentence ;
    Line2_one : Name -> NP -> Sentence ;
    Line2_1 : ListNP -> Adv ;
    Line2_1_one : NP -> Adv ;
    
    create_university : University -> Year -> NP ;
    
    create_universities_list : NP -> NP -> ListNP ;

    add_university : NP -> ListNP -> ListNP ;

    Line3 : Name -> Numeral -> Digits -> Sentence ;
    Line3_norank : Name -> Digits -> Sentence ;
    Line3_largest : Name -> Digits -> Sentence ;

    Final: Sentence -> Sentence -> Sentence -> Full_Sentence ;
    Final_without_line2 : Sentence -> Sentence -> Full_Sentence ;
    --Final_utan_residensstad: Sentence -> Sentence -> Sentence -> Full_Sentence ;


    CityObject : String -> City ;
    NameObject_vowel : String -> Name ;
    NameObject_consonant : String -> Name ;
    NameObject : String -> Name ;

    pn_masc : Name -> PN_String ;
    pn_fem : Name -> PN_String ;

    StringNameObject : String -> StringName ;
    UniversityObject : String -> University ;
    YearObject : String -> Year ;
    --RankObject : String -> Rank ;
    PopulationObject : Int -> Population ;

    mkNumeral1 : Numeral ;
    mkNumeral2 : Numeral ;
    mkNumeral3 : Numeral ;
    mkNumeral4 : Numeral ;
    mkNumeral5 : Numeral ;
    mkNumeral6 : Numeral ;
    mkNumeral7 : Numeral ;
    mkNumeral8 : Numeral ;
    mkNumeral9 : Numeral ;
    mkNumeral10 : Numeral ;

    mkDigit0 : Digits ;
    mkDigit1 : Digits ;
    mkDigit2 : Digits ;
    mkDigit3 : Digits ;
    mkDigit4 : Digits ;
    mkDigit5 : Digits ;
    mkDigit6 : Digits ;
    mkDigit7 : Digits ;
    mkDigit8 : Digits ;
    mkDigit9 : Digits ;

    mkDigits0 : Digits -> Digits ;
    mkDigits1 : Digits -> Digits ;
    mkDigits2 : Digits -> Digits ;
    mkDigits3: Digits -> Digits ;
    mkDigits4: Digits -> Digits ;
    mkDigits5: Digits -> Digits ;
    mkDigits6: Digits -> Digits ;
    mkDigits7: Digits -> Digits ;
    mkDigits8: Digits -> Digits ;
    mkDigits9: Digits -> Digits ;

    
    IntNumber : Int -> Number ;
    NumeralNumber : Numeral -> Number ;

    IntRank : Int -> Rank ;
    NumeralRank : Numeral -> Rank ;

    Number_To_Number : Number -> Number ;
    Rank_To_Rank : Rank -> Rank ;

    }
