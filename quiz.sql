CREATE TABLE questions_quiz (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_option INT
);

INSERT INTO questions_quiz (question_text, option1, option2, option3, option4, correct_option)
VALUES (
    "Python'da hangi veri tipi değiştirilemezdir?",
    "List",
    "Tuple",
    "Dictionary",
    "Set",
    1
),
(
    "Python'da 'range()' fonksiyonu ne döndürür?",
    "Liste",
    "Tuple",
    "Sözlük",
    "Range objesi",
    3
),
(
    "Python'da bir string'in tersini nasıl alabiliriz?",
    "reverse() fonksiyonuyla",
    "reversed() fonksiyonuyla",
    "Ters indeksleme kullanarak",
    "Ters döngü kullanarak",
    1
),
(
    "Python'da 'lambda' ifadesi ne işe yarar?",
    "Döngülerde kullanılır",
    "Kullanıcıdan input almak için kullanılır",
    "Anonim fonksiyon oluşturmak için kullanılır",
    "Dosya işlemlerinde kullanılır",
    2
),
(
    "Python'da 'try', 'except' ve 'finally' ne işe yarar?",
    "Kodun performansını arttırmak için kullanılır",
    "Hata yakalamak ve işlem yapmak için kullanılır",
    "Veritabanı işlemleri için kullanılır",
    "Özel fonksiyonlar oluşturmak için kullanılır",
    1
),
(
    "Python'da hangi komut bir döngüyü aniden sonlandırır?",
    "break",
    "pass",
    "continue",
    "exit",
    0
),
(
    "Python'da bir dosyayı okuma modunda açmak için hangi komut kullanılır?",
    "file_open('r')",
    "open_file('read')",
    "file_open('read')",
    "open('filename.txt', 'r')",
    3
),
(
    "Python'da 'map()' fonksiyonu ne işe yarar?",
    "Fonksiyonu bir listedeki her bir öğeye uygular",
    "Listeleri birleştirmek için kullanılır",
    "Sıralama yapmak için kullanılır",
    "Listeleri filtrelemek için kullanılır",
    0
),
(
    "Python'da 'pass' ifadesi ne işe yarar?",
    "Hiçbir şey yapmaz, geçişi sağlar",
    "Kod hata verdiğinde kullanılır",
    "Döngüyü sonlandırır",
    "Fonksiyonlarda geri dönüş değeri belirtmek için kullanılır",
    0
),
(
    "Python'da 'set' veri tipi neyi temsil eder?",
    "Diziyi temsil eder",
    "Kümeyi temsil eder",
    "Sözlüğü temsil eder",
    "Listeyi temsil eder",
    1
);

