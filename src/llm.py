from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, T5Tokenizer, T5ForConditionalGeneration
import torch


class model:
    def __init__(self, model_name, use_f16=False):
        allowed_models = ["google/flan-t5-small",
                          "google/flan-t5-large"]
        if model_name not in allowed_models:
            raise ValueError(
                f"Unexpected model name. Allowed models: {', '.join(allowed_models)}")
        if model_name.endswith("xl"):
            self.tokenizer = T5Tokenizer.from_pretrained(model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(
                model_name, device_map="auto", torch_dtype=torch.float16 if use_f16 else torch.float32)
        else:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def __call__(self, input_text, **kwargs):
        inputs = self.tokenizer(input_text, return_tensors="pt")
        default_kwargs = {
            'min_length': 256, 'max_new_tokens': 512, 'length_penalty': 2, 'num_beams': 16, 'no_repeat_ngram_size': 2, 'early_stopping': True
        }
        outputs = self.model.generate(**inputs, **default_kwargs)
        generated_text = self.tokenizer.batch_decode(
            outputs, skip_special_tokens=True)
        return generated_text[0]


# Test:
if __name__ == "__main__":
    try:
        generator = model("google/flan-t5-small")
        input_text = "Explain quantum tomography."
        generated_text = generator(input_text, min_length=256, max_new_tokens=512,
                                   length_penalty=2, num_beams=16, no_repeat_ngram_size=2, early_stopping=True)
        print(generated_text)
    except ValueError as e:
        print(f"Exception occurred: {str(e)}")
