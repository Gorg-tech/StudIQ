Wer kennt es nicht: In 2 Wochen steht die Prüfung in Rechnernetze an und man müsste eigentlich schon anfangen mit lernen. Aber niemand hat Lust, Hunderte Vorlesungsfolien auswendig zu lernen und so prokrasitiniert man, bis die Prüfung am nächsten morgen stattfindet und man bemerkt wie wenig man weiß.

Aber so muss es nicht laufen haben wir uns gedacht, und deshalb haben wir uns an die Entwicklung von StudIQ

Und damit hallo liebe Studierenden, sehr geehrter Herr Prof. Anke, wir präsentieren euch heute unseren Prototypen von StudIQ – einer webbasierten App, mit der Studierende der HTW Dresden ihre Prüfungen effizienter und spielerischer vorbereiten können.

Zuerst stellen wir euch dafür unser Produktkonzept vor, was unser Rahmen war, an den wir uns bei der Entwicklung halten haben, danach unsere Architektur und als letztes wird euch <Name> unseren Prototypen vorführen,

Kommen wir zum Produktkonzept: 
Als Prüfungsvorbereiter ist StudIQ in erster Linie für Studenten gemacht. Ihnen sollen durch spielerische Elemnte das Lernen für die Prüfung erlechtert werden. In zweiter Linie auch die Professoren, die qualitative Quizzes für ihre Studenten erstellen können.
So wollen wir Studenten durch einen einfachen Zugang zum Lehrmaterial und das Hinzufügen von spielerischen und kompetitiven Elementen zum Lernen motivieren. Das Lehrmaterial wird dabei größtenteils durch die Nutzer erzeugt, die Studenten.
- Denn die Quizzes werden von Studenten für Studenten erstellt, so ist die Aktualität der Themen am besten garantiert. Die Überprüfung der Quizzes erfolgt durch ein Votingsystem, indem Studenten nach dem Lösen des Quizzes dieses up-oder downvoten können, wie ihnen das Quiz gefallen hat.
- Die Quizzes lassen sich natürlich auch lösen, wobei es für die Abwechslung verschiedene Fragetypen gibt, z.B. Multiple-Choice oder Drag-and-Drop von Fragen und entsprechenden Antworten
- Ein weiteres Feature sind die persönlichen Statistiken, damit jeder Nutzer seine Statistiken und seine erreichten Punkte sehen kann.
- Für eine schnelle Orientierung lassen sich Quizze, Module, Lernsets oder Studiengänge auch gezielt über die Suchfunktion finden.
- Und eins der wichtigsten Elemente ist das Leaderboard, damit jeder sich mit anderen Lernenden vergleichen kann und dadurch motiviert wird noch besser zu werden um eines Tages an der Spitze zu stehen.

Unsere Architektur haben wir wie folgt gewählt: 
Wir entwickeln eine Web-App, da unserer Meinung nach so der Zugang zum Lernen am einfachsten und schnellsten ist. Für dessen Entwicklung haben wir als Frontend Vue verwendet, weil es uns am Einsteigerfreundlichsten erschien. Als Backend-Framework haben wir uns für Django entschieden, welches auch unsere Datenbank verwaltet, die SQLite verwendet. Als Schnittstelle zwischen dem Frontend-Client und dem Backend-Server dient das Django REST Framework.
Unsere Architektur ist darauf ausgelegt, skalierbar zu sein und neue Features wie z. B. gemeinsame Study-Groups einfach integrieren zu können.


Kommen wir zu einer kurzen Demo unseres Prototypen
...


Nun sind wir am Ende unserer kleinen Präsentation angekommen. Ihr seht, wir haben noch viel vor und wie bedanken und für eure Aufmerksamkeit.
Wir hoffen euch hat unsere Vorstellung unseres Prototypen gefallen und vielleicht seid ihr ja auch schon so gespannt wie wir, was StudIQ am Ende noch alles tun kann, um einen perfekt auf die Prüfung vorzubereiten.
