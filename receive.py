# Request receive script for RCFBBotTemplate

class Receiver():
    def __init__(self, request):
        self.received_time = request['entry'][0]['time']
        request = request['entry'][0]['messaging'][0]
        self.sender_messenger_id = request['sender']['id']
        if request.get('postback'):
            postbackHandler(request)
        elif request.get('message'):
            messageHandler(request)
        elif request.get('read'):
            readHandler(request)
        elif request.get('delivery'):
            deliveryHandler(request)
        else:
            self.request_type = None

    def postback_handler(request):
        self.timestamp = request['timestamp']
        self.request_type = 'postback'
        self.payload = request['postback']['payload']

    def message_handler(request):
        self.timestamp = request['timestamp']
        message_request = request['message']
        self.request_type = 'message'
        self.seq = message_request['seq']
        if message_request.get('attachments'):
            attachment = request['attachements'][0]
            self.message_type = attachment['type']
            payload = attachment['payload']
            if self.message_type == 'location':
                self.lat = payload['coordinates']['lat']
                self.long = payload['coordinates']['long']
            else:
                self.attachment_url = payload['url']
        else:
            self.message_type = 'message'
            self.text = message_request['text']
            if message_request.get('quick_reply'):
                self.message_type = 'quick_reply'
                self.quick_reply_payload = request['message']['quick_reply']['payload']

    def delivery_handler(request):
        self.request_type = 'delivery'
        self.seq = request['read']['seq']

    def read_handler(request):
        self.request_type ='read'
        self.timestamp = request['timestamp']
        self.seq = request['read']['seq']

    # RECEIVER GETTERS

    def get_received_time():
        return self.received_time

    def get_request_type():
        return self.request_type

    def get_sender_messenger_id():
        return self.sender_messenger_id

    def get_seq():
        # Available with Message, Delivery, and Read
        return self.seq

    def get_timestamp():
        # Available with Message and Read
        return self.timestamp

    # MESSAGE GETTERS

    def get_message_type():
        return self.message_type

    def get_text():
        return self.text

    def get_quick_reply_payload():
        return self.quick_reply_payload

    def get_attachment_url():
        return self.attachment_url

    def getCoordinates():
        # Returns tuple of coordinates
        return (self.lat, self.long)

    # POSTBACK GETTERS

    def get_payload():
        return self.payload
