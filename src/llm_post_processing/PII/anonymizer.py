import spacy
import re

class PII_anonymize:
  def __init__(self, spacy_mod = "en_core_web_sm"):
    self.model = spacy.load(spacy_mod)
    self.__patterns = {
        "<EMAIL>": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:\.[A-Za-z]{2,})?\b",
        "<IP_ADDRESS>": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "<PHONE_NUMBER>": r"\b(?:\+\d{1,3}[-\s]?)?(?:\(?\d{3}\)?[-\s]?)?\d{1,5}[-\s]?\d{4,}\b",
        "<BTC_ADDRESS>": r"(?<![a-km-zA-HJ-NP-Z0-9])[13][a-km-zA-HJ-NP-Z0-9]{26,33}(?![a-km-zA-HJ-NP-Z0-9])"

    }

  def __call__(self, text):
    doc = self.model(text)
    self.new_text = text
    self.__anonymize_regex()
    for entity in doc.ents:
      self.new_text = self.new_text.replace(str(entity.text), "<"+str(entity.label_)+">")
    return self.new_text

  def __anonymize_regex(self):
    for label in self.__patterns.keys():
      self.new_text = re.sub(self.__patterns[label], label, self.new_text)
    return self.new_text

  
if __name__ == "__main__":
  anonymise = PII_anonymize()
  text = "Hi I am John and my surname is Daniel, my Phone number: 8787878787878 you can reach me out at somes.546@some.some.some or 78.596.34.12"
  text = anonymise(text)
  print(text)