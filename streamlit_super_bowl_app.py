import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Define the Streamlit app
def main():
    # Load the CSV data into DataFrames
    super_bowls = pd.read_csv('data/super_bowls.csv')
    tv = pd.read_csv('data/tv_data.csv')
    halftime_musicians = pd.read_csv('data/halftime_show_artists.csv')

    # Display the first five rows of each DataFrame
    st.write("Super Bowls DataFrame")
    st.dataframe(super_bowls.head())

    st.write("TV DataFrame")
    st.dataframe(tv.head())

    st.write("Halftime Musicians DataFrame")
    st.dataframe(halftime_musicians.head())

    # Plot a histogram of point differences
    st.subheader("Histogram of Point Differences")
    plt.hist(super_bowls.difference_pts)
    plt.xlabel('Point Difference')
    plt.ylabel('Number of Super Bowls')
    st.pyplot(plt)

    # Display the closest game(s) and biggest blowouts
    st.subheader("Closest Game(s)")
    st.dataframe(super_bowls[super_bowls['difference_pts'] == 1])

    st.subheader("Biggest Blowouts")
    st.dataframe(super_bowls[super_bowls['difference_pts'] >= 25])

    # Join game and TV data, filtering out SB I because it was split over two networks
    games_tv = pd.merge(tv[tv['super_bowl'] > 1], super_bowls, on='super_bowl')

    # Create a scatter plot with a linear regression model fit
    st.subheader("Scatter Plot with Linear Regression Model Fit")
    sns.regplot(x='difference_pts', y='share_household', data=games_tv)
    st.pyplot()

    # Create a figure with 3x1 subplot
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    # Top subplot - Average Number of US Viewers
    axs[0].plot(tv.super_bowl, tv.avg_us_viewers, color='#648FFF')
    axs[0].set_title('Average Number of US Viewers')

    # Middle subplot - Household Rating
    axs[1].plot(tv.super_bowl, tv.rating_household, color='#DC267F')
    axs[1].set_title('Household Rating')

    # Bottom subplot - Ad Cost
    axs[2].plot(tv.super_bowl, tv.ad_cost, color='#FFB000')
    axs[2].set_title('Ad Cost')
    axs[2].set_xlabel('SUPER BOWL')

    # Improve the spacing between subplots
    plt.tight_layout()

    # Display the subplots
    st.subheader("Subplots")
    st.pyplot(fig)

    # Display all halftime musicians for Super Bowls up to and including Super Bowl XXVII
    st.subheader("Halftime Musicians")
    st.dataframe(halftime_musicians[halftime_musicians.super_bowl <= 27])

    # Count halftime show appearances for each musician and sort them from most to least
    halftime_appearances = halftime_musicians.groupby('musician').count()['super_bowl'].reset_index()
    halftime_appearances = halftime_appearances.sort_values('super_bowl', ascending=False)

    # Display musicians with more than one halftime show appearance
    st.subheader("Musicians with Multiple Halftime Show Appearances")
    st.dataframe(halftime_appearances[halftime_appearances["super_bowl"] > 1])

    # Filter out most marching bands
    no_bands = halftime_musicians[~halftime_musicians.musician.str.contains('Marching')]
    no_bands = no_bands[~no_bands.musician.str.contains('Spirit')]

    # Plot a histogram of number of songs per performance
    most_songs = int(max(no_bands['num_songs'].values))
    plt.hist(no_bands.num_songs.dropna(), bins=most_songs)
    plt.xlabel("Number of Songs Per Halftime Show Performance")
    plt.ylabel('Number of Musicians')
    st.subheader("Histogram of Number of Songs Per Performance")
    st.pyplot(plt)

    # Sort the non-band musicians by number of songs per appearance and display the top 15
    st.subheader("Top 15 Non-Band Musicians by Number of Songs Per Appearance")
    st.dataframe(no_bands.sort_values('num_songs', ascending=False).head(15))

# Run the Streamlit app
if __name__ == '__main__':
    main()
