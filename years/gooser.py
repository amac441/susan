from goose import Goose

class Gooser():

    def goosing(self, url):
        g = Goose()
        
        try:
            article = g.extract(url=url)
            response = {'title' : article.title , 
                'text' : article.cleaned_text[:500],
                'image': article.top_image.src}
        
        # maybe in the future we will add "Summarize Text" or "Generate Questions"
                
        except:
            a =1

        return response


