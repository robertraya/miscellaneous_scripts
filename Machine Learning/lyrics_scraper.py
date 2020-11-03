import lyricsgenius as lg

file = open("three_artists.txt", "w")

genius = lg. Genius('sZHVLtqoJEygMiovWzTG1TQ3GudEG1Gza7bk1Kyf6hkyNX51gPFFAWclfzzbm6a0', 
            skip_non_songs=True, 
            excluded_terms=["(Skit)", "(Live)"], remove_section_headers=True)

# GENIUS_CLIENT = 'Y6HQHsF406UzWoHzMg8PHxvTrWT8NQPJ7Zvmyu-Ar6BXTNGOzUkpYp-CQ318o_Vv'
# GENIUS_CLIENT_SECRET = 'sgIPd2IunMlfu5MdY-7KMkE1FrW0EKXr4MGf88yHxoEAKqCbqIjz_s3ER4J21b-mplKpM2EZRn9NASKeyqeN0Q'

artist = ['Frank Ocean', 'Cardi B', 'Snoop Dogg']

def get_lyrics(big, pac):
    i = 0
    for name in big:
        try:
            songs = (genius.search_artist(name, max_songs=pac, sort='popularity')).songs
            s = [song.lyrics for song in songs]
            file.write("\n \n".join(s))
            i+=1
            print(f"Songs grabbed: {len(s)}")
        except:
            print(f"Some exception at {name}: {i}")


get_lyrics(artist, 50)