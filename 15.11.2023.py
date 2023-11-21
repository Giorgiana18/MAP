# Importați bibliotecile necesare
import cv2
import imutils
import numpy as np
import pytesseract
 
# Specificați calea către executabilul Tesseract (tesseract_cmd)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
 
# Încărcați imaginea de la calea specificată
img = cv2.imread(r'C:\Imagini\inmatriculare.jpeg')

 
# Convertiți imaginea în alb-negru (grayscale)
#Imaginea color este convertită în imagine alb-negru pentru a reduce complexitatea prelucrării.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
#Aplicarea unui filtru bilateral pentru a reduce zgomotul în imagine. Parametrii controlază puterea filtrului și dimensiunea kernel-ului.
gray = cv2.bilateralFilter(gray, 13, 15, 15)
 
#Se utilizează algoritmul Canny pentru a identifica marginile în imagine. Parametrii sunt pragurile pentru detecția marginilor.
#Canny-ul scoate in evidenta contururile din imagine
edged = cv2.Canny(gray, 30, 200)
 
# Găsiți contururile din imagine
#cv2.findContours găsește contururile din imaginea Canny. imutils.grab_contours este folosit pentru a asigura
#compatibilitate între diverse versiuni ale OpenCV. Contururile sunt apoi sortate în funcție de aria lor, 
# iar primele 10 contururi mari sunt păstrate.
contur = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contur = imutils.grab_contours(contur)
contur = sorted(contur, key=cv2.contourArea, reverse=True)[:10]
 
# Inițializați variabila pentru a reține conturul identificat
screenCnt = None
 
#Se parcurg conturile și se utilizează cv2.approxPolyDP pentru a obține un contur cu aproximativ 4 laturi. 
# Acesta este considerat a fi conturul dorit pentru numărul de înmatriculare.
for c in contur:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    if len(approx) == 4:
        screenCnt = approx
        break
 
# Verificați dacă s-a identificat un contur
if screenCnt is None:
    detected = 0
    print("NU AM GASIT NICIUN CONTUR")
else:
    detected = 1
 
# Se creează o mască goală, iar conturul identificat este desenat pe această mască.
# Apoi, mască este aplicată imaginii originale pentru a obține imaginea cu conturul identificat.
 
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
 
# Aplicați mască pentru a obține imaginea cu conturul identificat
new_image = cv2.bitwise_and(img, img, mask=mask)
 
#Se găsesc coordonatele colțurilor conturului pentru a determina regiunea care conține numărul de înmatriculare.
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
 
#Se decupează regiunea din imaginea alb-negru care conține numărul de înmatriculare.
Crop = gray[topx:bottomx + 1, topy:bottomy + 1]
 
# Utilizați Tesseract pentru a recunoaște textul din regiunea decupată
text_numar = pytesseract.image_to_string(Crop, config='--psm 10')
 
#Se afișează numărul de înmatriculare detectat și se redimensionează imaginile pentru o afișare mai bună.
print("Numărul de înmatriculare detectat este", text_numar)
 
# Redimensionați imaginea și regiunea decupată și afișați-le
img = cv2.resize(img, (500, 300))
Crop = cv2.resize(Crop, (400, 200))
cv2.imshow('CROP', Crop)
 
# Așteptați apăsarea unei taste pentru a închide fereastra
cv2.waitKey(0)
cv2.destroyAllWindows()