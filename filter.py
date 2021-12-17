import pandas as pd

def main():

    df = pd.read_csv('books.csv')
    new_df = df.drop(columns=['isbn13', 'isbn10', 'thumbnail', 'description', 'published_year', 'average_rating', 'num_pages', 'ratings_count'])
    new_df= new_df.dropna(subset=['title'])
    new_df= new_df.dropna(subset=['authors'])
    new_df= new_df.dropna(subset=['categories'])

    print("Number of Data in Original Dataset", len(df), "\n Number of Data in Filtered Dataset:", 
       len(new_df), "\nNumber of Rows Deleted: ",
       (len(df) - len(new_df)))

    new_df.to_csv('books1.csv')

if __name__=="__main__":
    main()