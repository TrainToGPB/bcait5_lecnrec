import torch
import asyncio
from transformers import MT5ForConditionalGeneration, MT5Tokenizer


def set_inference():
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model_name = "traintogpb/mt5-large-kor-qa-generation-finetuned"
    tokenizer = MT5Tokenizer.from_pretrained(model_name)
    model = MT5ForConditionalGeneration.from_pretrained(model_name)
    model.to(device)
    return tokenizer, model, device


def generate_n_beams_qnas(context, tokenizer, model, device, n_beams=10):
    input_ids = tokenizer.encode_plus(
        context,
        padding="max_length",
        truncation=True,
        max_length=512,
        return_tensors="pt"
    ).input_ids.to(device)

    generated_ids = model.generate(
        input_ids,
        num_beams=n_beams,
        max_length=128,
        early_stopping=True,
        num_return_sequences=n_beams,
    )

    generated_qnas = []
    for generated_id in generated_ids:
        qa = tokenizer.decode(generated_id, skip_special_tokens=True)
        generated_qnas.append(qa)
    return generated_qnas


def make_nothing():
    question = '<no_question>'
    answer = '<no_answer>'
    return question, answer


def qna_postprocess(generated_qnas, n_qna=3):
    questions, answers = [], []
    for qa in generated_qnas:
        print(qa)
        try:
            question, answer = qa.split('?')
            question = question.strip() + '?'
            answer = answer.strip()

            if answer in question:
                question, answer = make_nothing()
            if any(existing_answer in answer or answer in existing_answer for existing_answer in answers):
                question, answer = make_nothing()

            if answer != '<no_answer>':
                questions.append(question)
                answers.append(answer)

            if len(answers) == n_qna:
                print(len(answers))
                break

        except ValueError:
            continue

    if len(answers) < n_qna:
        for _ in range(len(answers), n_qna):
            question, answer = make_nothing()
            questions.append(question)
            answers.append(answer)

    return questions, answers


def generate_qnas_sync(context):
    tokenizer, model, device = set_inference()
    generated_qnas = generate_n_beams_qnas(context, tokenizer, model, device, n_beams=10)
    questions, answers = qna_postprocess(generated_qnas)
    return questions, answers


async def questionize(summary):
    questions, answers = await asyncio.create_task(generate_qnas_sync(summary))
    return questions, answers


async def questionize_test(context):
    await asyncio.sleep(5)
    questions = ["Sample Question 1", "Sample Question 2", "Sample Question 3"]
    answers = ["Sample Answer 1", "Sample Answer 2", "Sample Answer 3"]
    return questions, answers


def main():
    context = """제2차 세계 대전이 일어난 원인은 제1차 세계 대전의 패배로 인한 독일 제국의 무기력한 붕괴와 
        대공황으로 인한 전세계적인 불안, 소련으로 대표되는 사회주의 세력의 확대에 대한 불안 등 명확하지 않고 복잡하다. 
        일반적으로 대공황에 따른 경제 위기로 부상한 파시즘과 이에 따른 베르사유 조약에 대한 바이마르 공화국의 반발 및 
        기존 세계 질서에서 만족할 만한 패권을 가지고 있지 않던 일본 제국과 이탈리아 왕국의 보상심리가 원인으로 알려져 있다. 
        결국 결론적으로 제1차 세계 대전의 수습과 전후 정리 과정에서 현실과 미래를 예단하지 못한 이해당사자들의 인지부조화가 
        쌓이면서 터진 제1차 세계 대전의 연장선상에 있는 전쟁으로 보는 의견이 학계의 주류로 올라섰다. 이 문단에서는 제2차 세계 대전이 
        발발하기까지 세계가 어떤 과정을 겪었는지에 대해 서술하고 있다."""
    
    questions, answers = questionize(context)
    print(f"questions: {questions}", f"answers: {answers}", end='\n')


if __name__ == "__main__":
    main()
