# kacykowanie
proj na kackyki

Spróbuj zczytać z jakichś wygładzonych danych (choćby twoich pdf) nuty albo ich znaczenie, do nocy spróbuję znaleźć pięciolinię w postaci <lewy górny; lewy dolny; prawy górny; prawy dolny> róg - albo 2 linie - górna i dolna, w takiej samej postaci i ewentualnie wykrycie niezidentyfikowanych nut na tej 5-linii

Jeszcze dobrze byłoby usunąć pięciolinię - to bardzo by pomogło w ropoznawaniu symboli, znaleźć grubość linii i odległość między liniami.
Tak, czytałem te papierki; Teraz chcę zrobić tak, że:
1) Binaryzuję obrazek - mam to, ale cieńko, z dużą liczbą ziarna, niedługo to ulepszę
2) Znajduję kąt, pod jakim pada pięciolinia - to już mam - biorę detektor linii
    cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    następnie sprawdzam średnią z kąta padania linii cosinusem od 40 do 60 percentyla - te najpowszechniejsze linie to pięciolinię, 
    a co za tym idzie, wokół mediany będą one kątowo (korzystam z równoległości - na razie biorę obrazki tylko z 1 pięciolinią)
3) Znajduję wiersze z 5-linią na obrazku i je zaznaczam używając horizontal projection. Jak tu dojdę, to pomyślę, co dalej.

OK: mam szkielet, dla pdf działa. Słaba binaryzacja, bez zmiany orientacji na razie. Teraz chcę zrobić orientację dla kilku prostych zdjęć i ulepszyć binaryzację, Staff removal mnie satysfakcjonuje, ulepszenie tego aspektu dojdzie, gdy zaczną się pięciolinie rysowane od szklanki albo złudzenia optyczne i nierówne linie. Całość masz w binarization.ipynb.
