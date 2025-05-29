#Modul to build a Mission

from dataclasses import dataclass
from message_system import Message, MessageType
from dataclasses import dataclass

@dataclass
class Officier:
    rank: str
    name: str
    unit: str

    image1: str
    image2: str
    image3: str
    def get_rank_value(self):
        return rank_values.get(self.rank, 0)  # Gibt 0 zurück, falls der Rang nicht gefunden wird    

officier_dwarkaar = Officier("Captain", "Dwarkaar", "226. Regiment", "sample1", "sample2", "sample3")
officier_bougle = Officier("General", "Bougle", "5. Division", "sample", "sample", "sample")
officier_klein = Officier("Leutnand", "Klein", "5. Aufklärer", "sample", "sample", "sample")
officier_braun = Officier("Captain", "Braun", "142. Regiment", "sample", "sample", "sample")
officier_weber = Officier("Major", "Weber", "187. Regiment", "sample", "sample", "sample")



""" Sample:
Message(
             type=MessageType.NORMAL,
             sender="EILBERICHT VON MAJOR WEBER",
             time="14.25",
             content="",   
        ), """

def sample_messages():
    return [
        Message(
            type=MessageType.WITNESSED,
            sender= officier_dwarkaar.name,
            time="14:23",
            content="Ich sehe durch mein Fernglas: Regiment 226 formiert sich neu hinter dem Hügel. Die Männer wirken erschöpft, aber diszipliniert. Oberst Mueller scheint die Lage im Griff zu haben."
        ),
        Message(
             type=MessageType.NORMAL,
             sender=officier_weber.name,
             time="14.25",
             content="General! Der linke Flügel ist unter schwerem Beschuss. Regiment 187 hat bereits 30% Verluste. Hauptmann Fischer bittet um sofortige Verstärkung oder Rückzugsbefehl!"   
        ),
        Message(
             type=MessageType.URGENT,
             sender=officier_braun.name,
             time="14.28",
             content="Regiment 142 hat Position Delta erreicht. Kein Feindkontakt. Warten auf weitere Befehle. Munition bei 80%."   
        ),
        Message(
             type=MessageType.NORMAL,
             sender= officier_klein.name,
             time="14.35",
             content="Feindliche Kavallerie gesichtet, etwa 200 Mann, 2km südöstlich von unserem Hauptquartier. Bewegungsrichtung unklar."   
        ),
    ]

# Wörterbuch zur Zuordnung von Rang zu Integer-Wert
rank_values = {
    "Korporal": 1,
    "Leutnand": 2,
    "Major": 3,
    "Captain": 4,
    "General": 5,
}


    

