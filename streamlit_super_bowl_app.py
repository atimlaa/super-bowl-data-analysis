import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Define the Streamlit app
def main():
    # Set page title and favicon
    st.set_page_config(page_title='Super Bowl Analysis', page_icon=':football:')

    # Load the CSV data into DataFrames
    @st.cache_data
    def load_data():
        super_bowls = pd.read_csv('data/super_bowls.csv')
        tv = pd.read_csv('data/tv_data.csv')
        halftime_musicians = pd.read_csv('data/halftime_show_artists.csv')
        return super_bowls, tv, halftime_musicians

    super_bowls, tv, halftime_musicians = load_data()

    # Add a title and subtitle
    st.title("Super Bowl Analysis")
    st.subheader("Exploring Super Bowl data, TV viewership, and halftime musicians")
    st.write("This is my first Streamlit project. Here I load, clean and explore Super Bowl data. The dataset used in this project was scraped and polished from Wikipedia. It is made up of three CSV files, game data, TV data and halftime musician data.")
    st.divider()

    # Display the first five rows of each DataFrame
    st.header("Super Bowls DataFrame")
    st.dataframe(super_bowls.head())

    st.header("TV DataFrame")
    st.dataframe(tv.head())

    st.header("Halftime Musicians DataFrame")
    st.dataframe(halftime_musicians.head())
    st.divider()

    # Plot a histogram of combined points
    st.subheader("Histogram of Combined Points")
    fig, ax = plt.subplots()
    ax.hist(super_bowls.combined_pts, bins=10, edgecolor='black')
    ax.set_xlabel('Combined Points')
    ax.set_ylabel('Number of Super Bowls')
    st.pyplot(fig)

    st.write("The overall analysis of combined points distribution reveals that the majority of matches conclude with a combined score falling within the 40 to 50 range, which can be considered an average range. The highest combined points recorded so far occurred in a match between the San Francisco 49ers and the San Diego Chargers, with a score of 75. The Super Bowl in 2023 holds the third-highest combined points, where Patrick Mahomes's Chiefs secured a victory against Jalen Hurt's Eagles with a score of 38-35, resulting in a combined score of 73.")
    # Display the closest game(s) and biggest blowouts in an expandable section
    col1, col2 = st.columns(2)

    with col1:
        st.header("Highest Scoring")
        st.dataframe(super_bowls[super_bowls['combined_pts'] > 70])

    with col2:
        st.header("Lowest Scoring")
        st.dataframe(super_bowls[super_bowls['combined_pts'] < 70])
    st.divider()

    # Plot a histogram of point differences
    st.subheader("Histogram of Point Differences")
    fig, ax = plt.subplots()
    ax.hist(super_bowls.difference_pts, bins=10, edgecolor='black')
    ax.set_xlabel('Point Difference')
    ax.set_ylabel('Number of Super Bowls')
    st.pyplot(fig)

    st.write("Analysing the distribution of points difference, it becomes apparent that most matches have a relatively narrow margin, usually between 0 and 10 points, indicating closely contested games. The closest match observed was between the New York Giants and the Buffalo Bulls, where the NY Giants secured a victory by just a single point!")

    # Display the closest game(s) and biggest blowouts in an expandable section
    col1, col2 = st.columns(2)

    with col1:
        st.header("Closest Game(s)")
        st.dataframe(super_bowls[super_bowls['difference_pts'] == 1])

    with col2:
        st.header("Biggest Blowouts")
        st.dataframe(super_bowls[super_bowls['difference_pts'] >= 25])
    st.divider()

    # Join game and TV data, filtering out SB I because it was split over two networks
    games_tv = pd.merge(tv[tv['super_bowl'] > 1], super_bowls, on='super_bowl')

    # Create a scatter plot with a linear regression model fit
    st.subheader("Scatter Plot with Linear Regression Model Fit")
    fig, ax = plt.subplots()
    sns.regplot(x='difference_pts', y='share_household', data=games_tv, ax=ax)
    ax.set_xlabel('Point Difference')
    ax.set_ylabel('Share of Household Viewers')
    st.pyplot(fig)

    st.write("The question of whether one team's dominance leads to lost viewership is a valid concern.")
    st.write("When a game exhibits a significant point difference, such as the Seattle Seahawks' dominant victory over the Denver Broncos with a 35-point difference (43-8), there is a possibility that some viewers might lose interest. A one-sided match, where one team clearly dominates the other, can potentially lead to boredom among viewers, prompting them to stop watching.")
    st.write("To investigate this matter, I created a scatter plot with a linear regression model fit using the seaborn package. The plot indicates a decreasing trend between household share (the average percentage of US households with a TV in use that were watching for the entire broadcast) and point difference. However, it's important to note that the evidence for a strong correlation is not conclusive due to the limited number of data points available.")
    st.write("In summary, while there appears to be a decreasing trend between point difference and viewership, we cannot definitively assert.")
    st.divider()

    # Create a figure with 3x1 subplot
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    # Top subplot - Average Number of US Viewers
    axs[0].plot(tv.super_bowl, tv.avg_us_viewers, color='#648FFF')
    axs[0].set_title('Average Number of US Viewers')
    axs[0].set_ylabel('Viewers')

    # Middle subplot - Household Rating
    axs[1].plot(tv.super_bowl, tv.rating_household, color='#DC267F')
    axs[1].set_title('Household Rating')
    axs[1].set_ylabel('Rating')

    # Bottom subplot - Ad Cost
    axs[2].plot(tv.super_bowl, tv.ad_cost, color='#FFB000')
    axs[2].set_title('Ad Cost')
    axs[2].set_xlabel('SUPER BOWL')
    axs[2].set_ylabel('Cost')

    # Improve the spacing between subplots
    plt.tight_layout()

    # Display the subplots
    st.subheader("Viewership and the ad industry over time")
    st.pyplot(fig)
    st.divider()

    # Display all halftime musicians for Super Bowls up to and including Super Bowl XXVII
    st.subheader("Halftime Shows")

    st.write("Over the years, the Super Bowl halftime show has undergone a remarkable transformation, evolving into a cultural phenomenon that commands high expectations for extraordinary performances by renowned artists.")
    st.write("When we look back at some of the earlier halftime shows, it becomes apparent that they were not on par with the extravagant and star-studded showcases we witness today.")
    st.write("Everything changed with Michael Jackson's groundbreaking performance during Super Bowl XXVII in 1993. His appearance drew an enormous viewership and demonstrated the immense value of the Super Bowl halftime show as a platform for entertainment. This pivotal moment prompted the NFL to recognize the potential of the halftime show and led them to secure big-name acts for future events.") 
    st.write("As a result, the modern Super Bowl halftime show has become a grand spectacle, eagerly anticipated by millions of viewers worldwide. It showcases top-tier musicians and performers, offering an unforgettable experience that has solidified its position as a significant cultural event in American television history.")
    st.dataframe(halftime_musicians[halftime_musicians.super_bowl <= 27])
    
    # Count halftime show appearances for each musician and sort them from most to least
    halftime_appearances = halftime_musicians.groupby('musician').count()['super_bowl'].reset_index()
    halftime_appearances = halftime_appearances.sort_values('super_bowl', ascending=False)

    # Display musicians with more than one halftime show appearance in an expandable section
    st.markdown("### Musicians with Multiple Halftime Show Appearances")
    st.dataframe(halftime_appearances[halftime_appearances["super_bowl"] > 1])

    # Filter out most marching bands
    no_bands = halftime_musicians[~halftime_musicians.musician.str.contains('Marching')]
    no_bands = no_bands[~no_bands.musician.str.contains('Spirit')]
    st.divider()

    # Plot a histogram of number of songs per performance
    most_songs = int(max(no_bands['num_songs'].values))
    fig, ax = plt.subplots()
    ax.hist(no_bands.num_songs.dropna(), bins=most_songs, edgecolor='black')
    ax.set_xlabel("Number of Songs Per Halftime Show Performance")
    ax.set_ylabel('Number of Musicians')
    st.subheader("Histogram of Number of Songs Per Performance")
    st.pyplot(fig)

    # Sort the non-band musicians by number of songs per appearance and display the top 15
    st.subheader("Top 10 Non-Band Musicians by Number of Songs Per Appearance")
    st.dataframe(no_bands.sort_values('num_songs', ascending=False).head(10))
    st.divider()

# Run the Streamlit app
if __name__ == '__main__':
    main()
