from typing import Tuple

from bookish.model import NounTranslation, VerbTranslation, SimpleTranslation, Translation


Result = Tuple[str, str]


def success(trans: Translation) -> Result:
    trans.successes += 1
    if not trans.successes % 3:
        trans.tier = trans.successes // 3
    return 'richtig!', 'success'


def post_check(trans: Translation, result: Result) -> Result:
    trans.attempts += 1
    trans.save()

    return result[0] + score(trans), result[1]


def score(trans: Translation) -> str:
    return f'<div class="pull-right">{trans.successes - 1}/{trans.attempts - 2}</div>'


def validate_noun(lithuanian: str, singular: str, plural: str) -> Result:
    try:
        trans = NounTranslation.get(
            NounTranslation.lithuanian == lithuanian,
            NounTranslation.singular == singular,
            NounTranslation.plural == plural or None,
        )
        result = success(trans)
    except NounTranslation.DoesNotExist:
        trans = NounTranslation.get(NounTranslation.lithuanian == lithuanian)
        result = (f"""
            {lithuanian} ≠ {singular}, {plural or '-'} <br>
            {trans.lithuanian} = {trans.singular}, {trans.plural or '-'}, {trans.comment or ''}
            """, 'danger')

    return post_check(trans, result)


def validate_verb(lithuanian: str, infinitive: str, present: str, past: str, perfect: str) -> Result:
    try:
        trans = VerbTranslation.get(
            VerbTranslation.lithuanian == lithuanian,
            VerbTranslation.infinitive == infinitive,
            VerbTranslation.present == present,
            VerbTranslation.past == past,
            VerbTranslation.perfect == perfect,
        )
        result = success(trans)
    except VerbTranslation.DoesNotExist:
        trans = VerbTranslation.get(VerbTranslation.lithuanian == lithuanian)
        result = (f"""
            {lithuanian} ≠ {infinitive}, {present}, {past}, {perfect} <br>
            {trans.lithuanian} = {trans.infinitive}, {trans.present}, {trans.past}, {trans.perfect}
            """, 'danger')

    return post_check(trans, result)


def validate_word(lithuanian: str, word: str) -> Result:
    try:
        trans = SimpleTranslation.get(
            SimpleTranslation.lithuanian == lithuanian,
            SimpleTranslation.word == word,
        )
        result = success(trans)
    except SimpleTranslation.DoesNotExist:
        trans = SimpleTranslation.get(SimpleTranslation.lithuanian == lithuanian)
        result = (f"""
            {lithuanian} ≠ {word} <br>
            {trans.lithuanian} = {trans.word}
            """, 'danger')

    return post_check(trans, result)


def validate(args):
    print(args)
    if "type" not in args:
        return
    if args.get("type") == "noun":
        return validate_noun(args.get("lithuanian"), args.get("singular"), args.get("plural"))
    if args.get("type") == "verb":
        return validate_verb(args.get("lithuanian"), args.get("infinitive"), args.get("present"), args.get("past"), args.get("perfect"))
    if args.get("type") == "word":
        return validate_word(args.get("lithuanian"), args.get("word"))