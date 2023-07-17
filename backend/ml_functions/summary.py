import torch
from pprint import pprint
import asyncio
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import sys
sys.path.append('./')
import grouping, text_to_sum


def set_inference():
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model_name = "junsun10/mt5-base-kor-paper-summary"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.to(device)
    return model_name


def summarize_sync(transcription, model_name):
    data = grouping.split_text_into_sentences(transcription)
    grouped_data = grouping.main(data)
    raw_summary = text_to_sum.inference_group(grouped_data, model_name)
    summary = text_to_sum.post_processing(raw_summary)
    return summary


async def summarize(transcription, model_name):
    summary = await asyncio.create_task(summarize_sync(transcription, model_name))
    return summary


async def summarize_test(transcription):
    await asyncio.sleep(5)
    summary = "Sample Summary"
    return summary


def main():
    transcription = """아는데 이게 왜 이런지 이론적으로 이게 말끔하게 설명이 안 되고 있었다면 그런 것들을 좀 더 잘 설명해 줄 수 있는 현실에 맞게 잘 설명해 줄 수 있는 그런 어떤 모델로서 요게 기능을 할 수가 있게 됩니다. 이런 매개효과나 매개효과를 포함한 어떤 모델들의 역할이 그런 것들이라고 생각을 하시면은 알겠습니다. 요게 이제 매개효과구요. 매개효과에는 두가지 종류가 있어요. 두가지 종류가 있는데 뒤에 나올테지만 뒤에도 하나는 이제 완전, 안뒤에 보면 다른걸까? 하나는 어디있니? 완전 매개. 그리고 다른 하나는 부분 매개. 이렇게 두가지가 있어요. 이 완전 매개와 부분 매개는 뭐냐면은 이 학교폭력이 자살 사고에 직접적으로 영향을 끼치는 것은 없고 학교폭력은 무조건 우울을 증가시키고 그래서 그 증가된 우울이 자살 사고를 증가시키게 된다라는게 이제 검증이 되게 된다면은 그거를 우리가 완전 매개라고 합니다. 즉 원래 우리가 생각을 했던 원인 변인인 학교폭력과 결과 변인인 자살 사고 두 변인간의 직접적인 관계가 없고 무조건 저 중간단위를 거쳐갈 때 우리가 그걸 완전 매개라고 하고요. 부분 매개 같은 경우에는 학교폭력이 우울을 심화시키고 그 심화된 우울이 자살 사고를 증가시키지만 동시에 그것만으로는 이 학교폭력이 자살 사고를 높이는 그거를 온전히 다 설명할 수가 없어. 학교폭력이 우울을 높여서 높아진 우울이 자살 사고를 높이기도 하지만 동시에 또 학교폭력도 이 자살 사고를 직접적으로 좀 높이는 역할을 하는 걸로 보여 그렇게 검증이 된다면 그거는 우리가 매개 중에서도 부분 매개라고 이제 이야기를 하게 됩니다. 이렇게 두 가지로 좀 나뉘게 되고요. 이제 뭐 그렇다. 이렇게 완전 매개, 부분 매개. 검증은 여러분 검증은 어렵지 않습니다. 검증은 되게 쉬워요. 쉽고 검증은 이제 총 이렇게 요 뭐라그러냐 요 단계를 거쳐가지고 우리가 매개효과를 검증을 하게 됩니다. 요 단계를 거치게 되는데 한번 하나씩 살펴보도록 하죠. 먼저 가장 첫 번째는 뭐겠어요. 저 학교폭력이라는 예측 변수가 원인 변수가 자살 사고라는 결과 변수, 종속 변수를 이렇게 두 가지만 놓고 봤을 때 단순해기 모델이죠. 단순해기 모델로 저 두 가지 변수만을 놓고 봤을 때 학교폭력이 자살 사고를 유의미하게 예측을 하는지 학교폭력이 높아지면 자살 사고가 유의미하게 높아지는지를 우리가 단순해기로 먼저 검증을

        해야겠죠. 그래서 요거를 이제 그림에서 확인을 하면 C라고 볼 수가 있어요. C에 있는 화살표 부분이에요. 요 루트를 우리가 먼저 검증을 하는 거죠. 1단계로 요거를 보고, 그리고 두 번째 단계는 뭐겠어요? 두 번째 단계는 C기기 확인이 됐으면 우리가 A를 검증을 해줘야겠죠. A를 검증을 해줄건데 학교폭력이 우울을 과연 유의미하게 예측을 하는지, 학교폭력이 우울을 유의미하게 예측을 하는지에 대해서 우울이 종속변이 되는 겁니다. 이 경우에는 우울을 종속변으로 놓고 학교폭력이 우울을 예측하는지 검증을 해줍니다. 단순하게 이 모델이 되겠죠. 그렇게 해서 저 A가 학교폭력이 우울을 유의미하게 예측하는지 혹은 높이는지 낮추는지 이것들이 이제 검증이 되고 나면은 그 다음 스텝으로는 우리가 뭘 검증을 해야겠어요? 우울이 자살 사고를 유의미하게 예측을 하는지 혹은 증명시키는지 감소시키는지 이론에 따라서 이런 목표에 좀 달라질 수가 있겠죠. 이런 것들은. 그리고 B를 우리가 검증을 하게 됩니다. 그래서 이렇게 세 가지가 다 검증, 요 세 가지 단순하게 분석을 우리가 실시를 하고 나면은 그리고 남은 그 다음 단계는 우리가 뭘 해야겠어요? 그 다음 단계는 이 학교폭력과 우울이 자살 사고를 예측하는 이 두 가지가 모두 한꺼번에 포함이 된 다중일기 모형을 우리가 검증을 해보게 됩니다. 그렇게 될 경우에 이제 어떻게 되냐면은 우울의 영향력, 그러니까 학교폭력이 우울에 영향을 끼쳐서 그 우울이 자살 사고에 영향을 끼치는 이 A, A만큼의 정확히는 뭐 A만큼이라고 엄밀히 말할 수는 없는데 어쨌든 이 학교폭력이 우울을 통해서 자살 사고에 끼치는 영향, 정확히는 이 길이죠. 전체 길 만큼의 영향력을 제외한, 제외하고도 이 학교폭력이 자살 사고를 유의미하게 예측하는지, 그러니까 이 C2다고 같은 경우에는 C2, 학교폭력이 이제 우울을, 우울이 끼치는 영향력을 통제하고도 여전히 유의미하게 자살 사고를 예측을 하는지를 우리가 검증을 하게 되고 만약에 매개효과가 유의미하다면 저 C2가 C에 비해서 어떻게 되겠어요? C2가 C에 비해서, C2가 기존 C에 비해서 유의미하게 줄어들겠죠. C2가 C에 비해서 줄어들 겁니다. 왜? 이게 원래는 이렇게 두 가지만 놓고 생각했을 때는 이 C만큼 얘가 설명을 했었는데 얘가 우울을 통해서 자살 사고를 설명하는 분량만큼을 통제를 하게 되니까 요만큼의 분량이 빠지게 되겠죠. 그러니까 그렇게 되면 요만큼의 분량을 뺀 값이 이제 C2가 될 건데 요 C2는

        그러면 어떻게 되겠어요. 그만큼 빠진 거니까 줄어들겠죠. C보다 그래서 유의미하게 줄어드는 거를 우리가 확인을 해주면 되겠습니다. 만약에 이렇게 줄어들었을 때 저 C2가 그래도 줄어들었음에도 불구하고 여전히 유의미하다. 여전히 유의미하다. 그러니까 우울을 통제하고도 여전히 학교폭력이 자살 사고를 그래도 줄어들었지만 예측을 하더라라고 한다면 그러면 뭐겠어요? 그러면 이제 부분 매개라고 이야기를 할 수가 있겠고요. 부분 매개다라고 이야기를 할 수가 있겠고 저 학교폭력이 자살 사고를 더 이상 유의미하게 예측하지 않았다. 이렇게 우울을 통제했더니 그렇게 되면 우리가 뭐라고 이야기할 수 있는 거예요? 완전 매개다라고 이제 이야기를 할 수가 있겠습니다. 다만 여기에서 이 1단계에서 1단계에서 1단계에서 기존에 C만 검증을 하는 거죠. 단순하게 모형으로. 이 1단계를 검증을 했을 때 이게 유의미하지 않을 수도 있거든요. 아예 팩도 없는 경우에는 보통 거의 그냥 가능성이 없다고 보면 되고 유의성 검증이라는 게 뭐예요? 확률적인 의사결정이잖아요. 확률적인 의사결정이니까 이게 좀 유의미하지는 않은데 그래도 회귀 개수가 충분히 있고 이런 경우들이 조금 있을 수가 있어요. 그래서 그런 경우에는 나머지 단계를 좀 진행을 해보셔야 됩니다. 나머지 단계를 좀 진행을 해가지고 이 2, 3, 4 단계에서 유의성이 검증이 되면은 이것도 우리가 매개 효과가 존재한다라고 좀 이야기를 할 수가 있어요. 1단계의 저 C가 무조건 꼭 통계적으로 유의미할 필요는 없습니다. 다만 이 말이 저 학교폭력과 자살 사고가 정말 아무런 관련도 없더라. 진짜 그냥 봤을 때 회귀 개수도 거의 0의 수렴을 하고 있고 팩도 없었다라고 한다면은 사실 뭐 그 뒤에 단계는 뭐 진행을 할 필요는 없겠죠. 그렇게 되면은 저기 뭐 매개 효과가 있다라고 나올 리가 없기 때문에 그런 경우에는 뭐 보지 않아도 되겠지만 저 유의성이라는 거에 너무 목을 멜 필요는 없다. 1단계에서 그렇게 정도만 요거를 좀 이해를 하시면은 되겠습니다. 이렇게 좀 이해를 하면 되고요. 나머지 내용들은 제가 설명을 했던, 설명을 했던 내용들이라고 보시면 되겠습니다. 이렇게 보시면 되고. 그래서 총 3번의, 총 3번의 검증을 하게 됩니다. 3번의 검증을 하게 되고. 그리고 마지막으로 이렇게 이 각 단계별 검증을 우리가 하고 나서 이제 뭘 해줘야 되냐면은 여기서 말하는 이 간접효과라는 건 뭐냐면요. 제가 말했던 학교폭력이 O를 거쳐서 자살 사고에 끼치는 영향이 있죠. 학교폭력이 O를 거쳐서 자살 사고에 끼치는, 그러니까 학교폭력이 끼치는 영향이긴 한데 얘가 다이렉트로 자살 사고에 가는 게 아니라 O를 거쳐가는 저거를 우리가 간접효과라고 이제

        이야기를 하거든요. 저 간접효과의 크기는 그럼 우리가 어떻게 추정을 할 수가 있냐면은 학교폭력이 우울을 예측하는 저 A와 그리고 우울이 자살사고를 예측하는 근데 여기서 이 B같은 경우에는 이 우울이 자살사고를 예측하는 B같은 경우에는 이 단순행기로 요걸 보는게 아니라 얘랑 같이 다중행기로 모델을 넣어가지고 이제 보게 됩니다. 이 B의 개수 같은 경우에는 왜냐면 거쳐서 가는 B에 우리가 관심이 있는 거기 때문에 거쳐서 가는 것에 관심이 있는 것이기 때문에 다중행기로 보게 되고요. 즉 학교폭력을 통제한 우울이 자살사고에 학교폭력을 통제했을 때 우리 자살사고에 기찬 영향을 요 B. 이 A와 B의 회기개수의 곱으로 우리가 간접효과의 크기를 추정을 할 수가 있어요. 이 회기개수 베타를 곱해주면 됩니다. A와 B의 회기개수를 베타를 곱해주면 되고요. 그렇게 되면은 우리가 간접효과의 크기를 추정을 할 수 있고 이 간접효과의 유의성을 우리가 검증을 또 실시를 할 수가 있어요. 간접효과의 유의성 검증을 실시를 할 수가 있는데 그거는 이제 SPSS에서는 안 돼요. SPSS에서는 요거를 하는 메뉴나 요런 것들이 없고 별도의 뭐 다른 프로그램을 사용을 하시거나 아니면은 인터넷 사이트 중에 요 간접효과 요 유의성 검증 소벨리 지검증인데 요거를 해주는 데이터를 입력하면 요거를 해주는 그 사이트가 있거든요. 그 사이트에 가서 하셔도 됩니다. 별도의 프로그램을 쓰기가 번거롭다면은 요 사이트 가서 하는 것까지 제가 오늘 좀 보여드리도록 할게요. 그러면은 한번 봅시다. 가설 요거. 가설은 요렇게 총 3가지 단계의 가설을 우리가 검증을 하게 되는 거죠. 학교폭력 피해 경험이 피해자들의 자살 사고를 증가시킨다. 뭐였죠 이게? 이 단순의 기고형으로 봤을 때 학교폭력에서 자살 사고가 나가요. 보면 C였죠 이게. C. 요게 가설 1이고 두번째 가설은 뭐였어요? 학교폭력 피해 경험이 피해자들의 우울성을 증가시킨다. 단순의 기고형으로 요것도 봤죠? A. 그리고 마지막은 뭐예요? 학교폭력 피해 경험이 우울을 통해서 자살 사고를 증가시킨다. B. 이렇게 세번의 우리가 검증을 하게 되고 이렇게 됐을 때 요 C 다시. 아까는 C2라고 써 있었던 요게. 우울을 통제했을 때 학교폭력이 자살 사고를 끼치는 C 프라임이나 아니면 C2 같은 경우에 이제 어떻게 되는 거예요? 얘는 C에 비해서 감소하게 된다. 감소하게 된다. 매개효과가 유의미하다면 이렇게 생각을 해주시면 되겠습니다. 요 3가지의 검증을 하게 될 거고 요것들은 사실 뭐 여러분들이 바로 할 수가 있어요. 제가 보여주지 않더라도 그냥 여러분들이 했던 지금까지 해왔던 그 회귀 검증이기 때문에 한번 같이 보도록 합시다. 요거 하는 거 좀 볼게요.

        SPSS 실행해 주시고, 우리가 지금까지 했던 그 회기 분석 데이터 세트 있죠? 그거 열어주시면 되겠습니다. 열어주시면 되고요. 자, 됐을 때, 일단 모델을 좀 만들어야겠죠? 모델을 만들어야 되는데, 이제 이론적으로 어떤 모델이 좀 맞을까? 봅시다. 뭔가 이 어떤 그, 이렇게 가죠. 저의, 저의 모델입니다. 저의 모델은 뭐냐면은, 자존감이, 부정적인 자존감이, 높은 아이들이, 높은 사람들이, 우울해요. 우울한 아이들이, 높은 사람들이, 우울해요. 우울해져, 우울한 경향성이 있어. 우울한 경향성이 있는데, 이게 왜 그러냐? 사실은 왜 그러냐? 이 부정적인 자존감이 오하기 때문에, 외로움을 심화시키기 때문에, 외롭다. 외롭다라고, 외로움을 심화시키기, 뭔가 있는 거 틀린 거 같은데, 어쨌든. 외로움을 심화시키기 때문에, 그래서 우울해진다. 단순, 이렇게 단순한 관계가 아니라, 이게 거쳐서 이렇게 가는, 이런 매개의 효과가 포함된, 그런 관계다라는 게, 이제 저의 모델입니다. 이거, 이 경우에, 이걸 한번 우리가 검증을 해보도록 할게요. 먼저, 자존감이 우울로 가는, 이 루트를 한번 우리가, 의미성을 검증을 해봐야겠죠. 우리가 그냥 하던 거 하면 됩니다. 회기분석 선형에서, 단순 회기분석 실시를 하면 되겠죠. 부정적인 자존감이, 우울을 예측하는, 우울을 예측하는, 이 모델을 만들어가지고, 바로 그냥 검증을 하도록 할게요. 다른 모델은 필요 없이, 단순 회기가 계속했던 거니까. 자, 이렇게 해서 봤을 때, 모델, 모델이, 모델이 유의미하죠. 모델이 유의미하고, r제곱 값이, .12, 이 정도 나오고, 유의 확률, 이렇게 해서, 이 c값, 이 c의 베타 값이 지금 몇이 나오게 돼요? 자존감, 부정이, 우울로 가는, 이 베타 값이, .868, 0.868이 나오게 됩니다. 0.868, 이렇게 해서, 이 경우에는 이제, 우리가 이번에 이거 할 때는, 이, 스탠다드 에러, 이 값도 우리가 같이 포함해서 좀 적도록 할게요. 스탠다드 에러 값은, 0.052, 이거는 우리가 왜 따로 적어두냐면은, 이따가 그, 소개를 지검증할 때, 요거, 요거, 스탠다드 에러 값을 우리가, 표준 도착 값을 같이 적어두면은, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052,

        좀 입력을 해줘야 돼가지고 같이 적어줍니다. 여기 있는 값이에요. 여기 표준화 오류라고 저는 여기 나와있는 여기 있는 값입니다. 그리고 베타 값은 이 비표준화 갯수를 적어주시면 됩니다. 비표준화 갯수를 적어주시면 되고 수가제치 검증할 때 비표준화 갯수가 필요하기 때문에 이렇게 해주시면 되고 자 이렇게 해서 요 루트를 우리가 해봤고 유의미하다 확인을 했고 자 그럼 이제 뭘 해봐야겠어요. 자존감이 그 외로움에 과연 외로움을 유의미하게 높이는 부정적인 자존감이 높아질 때 외로움이 과연 유의미하게 높아지는지. 요게 관계가 안 좋을 때 높아지는 거 맞죠? 부정적인 자존감이 높아지면 우울해지고 이게 높으면 안 좋은 것 같아. 자 그러면 이번에는 요 루트를 한번 요 루트를 검증을 해 볼게요. 자 폐기분석 선형으로 들어가서 종속변수만 바꿔주면 되겠죠? 이게 우울이 아니라 뭐가 돼야 돼요? 외로움이 돼야겠죠? 똑같이 분석을 해주면 되고요. 자 분석을 했을 때 간접효과 확인을 하고 유의미하고 폐기분석 장인이 유의미하게 나오죠? 요 경우에 유의미하고 비표준화 갯수가 0.810 되고 스탠다드대로는 0.058 우리가 확인했습니다. 자존감, 부정적인 자존감이 높아질수록 외로움도 어떻게 되는 거예요? 외로움도 증가한다. 외로움도 증가한다는 걸 우리가 확인을 해 줄 수가 있었고요. 이제 마지막으로 세번째, 세번째에서 요걸 한꺼번에 할 거예요. 요거랑 요거 요 C2, C2까지 우리가 한꺼번에 확인을 해 줄 겁니다. 자 요건 우리가 위계적 폐기분석의 모양을 사용을 해서 해주면 되겠죠? 종속변수는 일단 뭐가 되야겠죠? 우울이 돼야겠죠? 저 모델에 따르면 얘가 종속변수가 될 거고요. 첫번째 모델에서, 첫번째 모델은 어떻게 돼야 돼? 얘가 얘를 예측하는, 부정적인 자존감만으로 우울을 예측하는게 첫번째 모델이 될 거고 두번째 모델이 뭐가 되겠어요? 여기에 외로움이 추가되는, 외로움이 추가가 됐을때도 과연 유의미하게 예측을 한지 우리가 확인해 보도록 하겠습니다. 요렇게 블록을 두개로 나눠서 첫번째 블록에 자존감 부정, 그리고 두번째 블록에다가 매개변수라고 우리가 생각되는 저 매개변수를 넣어 줘가지고 종속변수는 우울이고, 이렇게 해서 분석을, 실행을 하도록 할게요. 자, 여기서는 그거 해봐야겠지? 모델이 더 좋아지는지는 한번 확인을 해주도록 하겠습니다. 이거 알제오 변화를 체크를 해가지고 모델이 더 좋아지는지, 모델이 더 좋아지네요. 모델이 더 좋아지는지 확인을 좀 해주도록 하고 그리고 나서 우리가

        각각의 획의개수를 좀 보도록 하겠습니다. 일단은 이 부분의 획의개수로 확인을 해야겠죠? 이 부분의 획의개수는 뭐예요? 여기에서 외로움이 저 5를 예측하는 이 획의개수, 이 부분이죠? 이 부분이 아까 ABC로 나눴을 때는 B부분이 되는 겁니다. B부분이 지금 몇인거예요? 그러니까 0.47 요거의 의미는 그러니까 뭐예요? 자존감이 외로움을 통해서 우울로... 아, 간접효과는 요거의 곱이고 요거 자체의 의미가 어떻게 되냐면 자존감이 우울에 끼치는 영향력을 배제하는 상태에서 외로움이 우울에 가는 영향이라고 보시면 되겠습니다. 이게 통제된 상태에서, 요 숫자의 의미고 표준화 우울값은 0.03인게 확인이 되네요. 요렇게 이제 해주고, 이제 C2, C프라임 값도 우리가 확인을 해줘야겠죠? 여기 저기 보면은 이제 자존감 부정의 값이 이렇게 나와있죠? 어떻게 돼있어요? 분명히 확실히 감소해있죠? 확실히 감소해있는 걸 우리가 확인을 해줄 수가 있고요. 이 경우에 일기계수는 몇이죠? 0.556 그리고 표준화, 표준호차가 0.03 자 요렇게 우리가 값들을 확인을 해줄 수가 있었고 일단은 요렇게 했을 때, 요 세가지, 세가지 단계의 가설들이 모두 어떻게 됐어요? 세가지 단계의 가설들이 모두 유의미성이 검증이 됐기 때문에 우리가 이 외로움이 자존감과 우울간의 관계를 어떻게 한다고 볼 수가 있어요. 네 개를 하고 있는 걸로 일단 보여집니다. 그러면 우리가 여기에서 자존감이 외로움을 통해서 우울에 끼치는 영향력은 어떻게 우리가 계산을 할 수가 있어요? 일단은 요 두개의 베타값을 곱하면은 자존감이 외로움을 통해서 우울에 가는 간접효과의 크기를 우리가 곱으로 추정을 해줄 수가 있습니다. 네 곱하는 거는 뭐 여러분들 계산기로 바로 할 수 있죠? 요거는 그냥 알아서 곱하시면 되고 이제 곱하면 되는데 중요한 건 이제 이 간접효과의 크기, 이 간접효과가 이 간접효과의 크기에 대한 우리가 유의미성도 검증을 해줘야 될 거예요. 요거까지 해야 이제 이 간접효과에 대한 검증이 끝난다고 볼 수가 있는데 그래서 우리가 소벨지검증을 실시를 해줄 거고 요 제가 올린 pdf에도 사이트가 적혀있을 텐데 사이트에 들어가보도록 하겠습니다.

        예, 사이트. 어, 항상 이거 들어갈 때마다 걱정돼. 혹시 이거 터지지 않았을까. 이거 운영하는 사람이 뭔가 자기 서버 빈을 운영하는 건데, 어, 닫아버릴 수도 있잖아. 그렇다면 어떡하지? 막 이런. 네, 다행히 안 닫혔네요. 네, 안 닫혔는데. 자, 여기에서 보면은 우리가 여기에다가 값을 입력을 해주면 돼요. 여기에다가 값을 입력을 해주면 되는데, 여기 보면은 이렇게 어떤 값을 입력을 해야 되는지 여기 이렇게 적혀있습니다. 어, 입력해야 되는 값이 여기 적혀있고, 여기에서 보면 우리는 뭘 해줘야 돼요? 여기 a, a가 뭐야? a가 아까 써놓은 거 0.810, 0.810 베타 갯수. a에다가 0.810 적어주고, b는 뭐예요? b는 이렇게. 여기에서 여기로 가는 0.417 적어주고요. 그리고 이거는 sa는 뭐냐면은 표준호차, 아까 적어놨던 표준호차를 적어주면 됩니다. a의 표준호차는 0.049였죠. b의 표준호차는 몇이었지? 0.04. 자, 이렇게 적어주면 되고요. 이렇게 적어주고, 그리고 이것들이 여기 보면은 제가 뭐 적어야 되는지, 뭐 적어야 되는지 여기에다가 써놨어요. 뭐 이렇게 써놨으니까 나중에 혹시 그 나중에는 나중에 사이트 들어가지고 어떻게 해야됐더라 이렇게 헷갈리시는 분들은 여기 그냥 bbk 이렇게 제가 친절하게도 이렇게 뭐를 해야 되는지 이렇게 표기를 해놨기 때문에 이런식으로 이제 확인을 해주면 되고요. 여기에 확인을 해주면 되고, 이 5번, 6번, 7번에 소벨의 지검증 값이 나오게 됩니다. 이 테스트 스태티스틱에 나오는 값이 통계치고요. 소벨의 소벨 값이라고 하고 통계치고, 그리고 이거는 통계치의 표준호차. 그리고 여기에는 이제 p-value, 그러니까 유의, 유의 확률이 이제 나오게 되는데 이 유의 확률을 보고 우리가 간접효과가 과연 유의미한지를 이걸로 최종적으로 확인을 해주면 되겠습니다. 여기에서 calculation, calculate 눌러줄게요. 눌러주게 되면 이렇게 이제 결과가 나오게 되죠. 이게 이제 소벨의 z 값이라고 생각을 해주시면 되고, 여기 통계치고, 그 옆에 p-value는 지금 0으로만 나오네. 아마 0.001 미만이라고 나오는 것 같죠. 그러니까 지금 간접효과가 유의미하다라는 게 이렇게 이제 확인이 되고 있습니다.

        되고 있고 나머지 이쪽에 값들은 저도 요거에 대해서는 사실은 정확히 잘 몰라요. 소베네치 검증을 보통 매개효과를 검증을 할 때 매개효과의 간접효과를 검증을 할 때 사용을 하기 때문에 이 위에 것만 좀 확인을 해주시면 되고 여기에서 또 이렇게 Z값 그리고 P-value 값 확인을 해가지고 요까지 여러분들이 보고를 해주시면 되겠습니다. 요 매개효과 검증을 해서 검증을 할 때 요까지 보고를 해주시면 되겠습니다. 자 그러면은 요것도 그래도 우리가 오늘 시간이 많이 없지만 여러분들 그래도 직접 한번 해보긴 해봐야겠죠. 해봐야 이것도 여러분들이 기억이 좀 남기 때문에 자 그럼 우리도 항상 하던 대로 어떻게 해야 돼? 각자의 좀 모델을 만들어서 각자의 모델을 한번 좀 만들어보고 각자의 이론적인 모델을 만들어보고 이론적인 모델 매개효과 모델에 대해서 검증까지 한번 지금 실시를 해보도록 하겠습니다. 바로 해보도록 할게요. 여러분들 시작하겠습니다. 혹시 뭔가 잘 안되거나 궁금한거 있거나 하나는 그냥 손 들거나 저 불러주셔가지고 질문하시고 아니면 가서 제가"""
    
    model_name = set_inference()
    summary = summarize_sync(transcription, model_name)
    pprint(summary)

if __name__ == "__main__":
    main()
