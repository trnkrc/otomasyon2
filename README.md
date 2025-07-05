# PDF Metraj API

Bu servis, altyapi projelerine ait PDF dosyalarindan otomatik metraj verisi cikarir.

## Kurulum
```
pip install -r requirements.txt
```

## Calistirma
```
uvicorn main:app --reload
```

## API
**POST /extract-metraj**  
PDF dosyasini gonderin, JSON metraj verisi alin.

---

Ilk surumde sadece basit Ø ve L degerlerini okur. Sonraki adimlarda baca no, zemin kotu ve akar yonune gore esleme eklenecek.
