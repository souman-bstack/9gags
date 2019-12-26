import datetime
import mongoengine

class Gag(mongoengine.Document):
    """Gag details are stored here"""
    content_type = mongoengine.StringField(required=True)
    url = mongoengine.StringField(required=True)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    tags = mongoengine.StringField()

    def save_gags(gags):
        for gag in gags:
            existing_gag = Gag.objects(url=gag['url']).first()
            if existing_gag == None:
                tags = gag['tags']
                gag_tags = []
                for tag in tags:
                    gag_tags.append(tag['key'])
                newGag = Gag(content_type=gag['type'], url=gag['url'], tags=', '.join(gag_tags))
                newGag.save()
            else:
                existing_gag.updated_at = datetime.datetime.now
                existing_gag.save()

    def get_gags(type, count):
        input_mapping = dict({'IMAGE': 'Photo', 'GIF': 'Animated', 'VIDEO':'EmbedVideo'})
        gags = None
        if count <= 0:
            print("Count should be positive")
            raise Exception("Count should be positive")
        if type in input_mapping.keys():
            object_type = input_mapping[type]
            gags = Gag.objects(content_type=object_type).order_by('-updated_at')[:count]
        elif type == "OVERALL":
            gags = Gag.objects().order_by('-updated_at')[:count]
        if gags == None:
            print("Enter valid gag type")
        else:
            for gag in gags:
                print(gag.url, gag.tags)
