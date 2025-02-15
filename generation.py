import uuid



def gen_link(chatID):



    unique_id = uuid.uuid5(uuid.NAMESPACE_URL, str(chatID))




    bot_username = "AnonymusQBot"
    deep_link = f"http://t.me/{bot_username}?start={unique_id}"

    return deep_link


