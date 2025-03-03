from customers.models import Client

async def add_client_to_db(user):
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    subscribed = True

    client, created = Client.objects.get_or_create(user_id=user_id)
    if created:
        client.first_name = first_name
        client.last_name = last_name
        client.username = username
        client.subscribed = subscribed
        client.save()
    return client
