import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="IPL Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")

    # Standardize column names
    matches.columns = matches.columns.str.strip().str.lower()
    deliveries.columns = deliveries.columns.str.strip().str.lower()

    return matches, deliveries

matches, deliveries = load_data()

# --- Page Title ---
st.title("🏏 IPL Data Analysis Dashboard")
st.markdown("Data source: Kaggle IPL Dataset (`matches.csv` & `deliveries.csv`)")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
selected_team = st.sidebar.selectbox("Select Team", sorted(matches['team1'].dropna().unique()))
selected_season = st.sidebar.selectbox("Select Season", sorted(matches['season'].dropna().unique()))
team1 = st.sidebar.selectbox("Team 1 (Head-to-Head)", sorted(matches['team1'].dropna().unique()))
team2 = st.sidebar.selectbox("Team 2 (Head-to-Head)", sorted(matches['team2'].dropna().unique()))

# --- Filtered Matches Table ---
filtered_matches = matches[
    (matches['season'] == selected_season) &
    ((matches['team1'] == selected_team) | (matches['team2'] == selected_team))
]

st.subheader(f"📅 Matches Played by {selected_team} in {selected_season}")
st.dataframe(filtered_matches[['date', 'team1', 'team2', 'winner', 'venue']])

# --- Overall Wins ---
st.subheader("📊 Overall Wins by Each Team")
wins = matches['winner'].value_counts().reset_index()
wins.columns = ['Team', 'Wins']
fig = px.bar(wins, x='Team', y='Wins', color='Team', title='Total Wins by Each Team')
st.plotly_chart(fig)

# --- Toss Decision ---
st.subheader("🧢 Toss Decision Analysis")
toss = matches['toss_decision'].value_counts()
fig2, ax2 = plt.subplots()
sns.barplot(x=toss.index, y=toss.values, ax=ax2)
ax2.set_title("Toss Decision: Bat vs Field")
st.pyplot(fig2)

# --- Top Batters by Runs ---
st.subheader("🏏 Top 10 Batters (by Runs)")
top_batter = deliveries.groupby('batter')['batsman_runs'].sum().nlargest(10)
fig3 = px.bar(top_batter, x=top_batter.index, y=top_batter.values, labels={'x': 'Batter', 'y': 'Runs'}, color=top_batter.index)
st.plotly_chart(fig3)

# --- Top Batters by Strike Rate ---
st.subheader("🔥 Top 10 Batters by Strike Rate (min 200 balls)")
balls_faced = deliveries.groupby('batter')['ball'].count()
runs_scored = deliveries.groupby('batter')['batsman_runs'].sum()
strike_rate = (runs_scored / balls_faced) * 100
qualified_strike_rate = strike_rate[balls_faced >= 200].sort_values(ascending=False).head(10)
fig_sr = px.bar(qualified_strike_rate, x=qualified_strike_rate.index, y=qualified_strike_rate.values,
                labels={'x': 'Batter', 'y': 'Strike Rate'}, color=qualified_strike_rate.index)
st.plotly_chart(fig_sr)

# --- Top Bowlers by Wickets ---
st.subheader("🎯 Top 10 Bowlers (by Wickets)")
valid_dismissals = ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
wickets = deliveries[deliveries['dismissal_kind'].isin(valid_dismissals)]
top_bowlers = wickets['bowler'].value_counts().head(10)
fig4 = px.bar(top_bowlers, x=top_bowlers.index, y=top_bowlers.values, labels={'x': 'Bowler', 'y': 'Wickets'}, color=top_bowlers.index)
st.plotly_chart(fig4)

# --- Top Bowlers by Economy ---
st.subheader("💸 Top 10 Bowlers by Economy Rate (min 300 balls)")
bowler_balls = deliveries.groupby('bowler')['ball'].count()
bowler_runs = deliveries.groupby('bowler')['total_runs'].sum()
economy = (bowler_runs / (bowler_balls / 6))
qualified_economy = economy[bowler_balls >= 300].sort_values().head(10)
fig_econ = px.bar(qualified_economy, x=qualified_economy.index, y=qualified_economy.values, labels={'x': 'Bowler', 'y': 'Economy'}, color=qualified_economy.index)
st.plotly_chart(fig_econ)

# --- Most Sixes & Fours ---
st.subheader("🔨 Most Sixes & Fours")
sixes = deliveries[deliveries['batsman_runs'] == 6]['batter'].value_counts().head(10)
fours = deliveries[deliveries['batsman_runs'] == 4]['batter'].value_counts().head(10)

col_six, col_four = st.columns(2)
with col_six:
    st.markdown("### Most Sixes")
    fig_six = px.bar(sixes, x=sixes.index, y=sixes.values, labels={'x': 'Batter', 'y': 'Sixes'}, color=sixes.index)
    st.plotly_chart(fig_six)

with col_four:
    st.markdown("### Most Fours")
    fig_four = px.bar(fours, x=fours.index, y=fours.values, labels={'x': 'Batter', 'y': 'Fours'}, color=fours.index)
    st.plotly_chart(fig_four)

# --- MVP Awards ---
st.subheader("🏅 MVP (Most Player of the Match Awards) Per Season")
mvp = matches[matches['season'] == selected_season]['player_of_match'].value_counts().head(5)
fig8 = px.bar(mvp, x=mvp.index, y=mvp.values, labels={'x': 'Player', 'y': 'Awards'}, color=mvp.index)
st.plotly_chart(fig8)

# --- Head to Head ---
st.subheader(f"⚔️ Head-to-Head: {team1} vs {team2}")
h2h = matches[((matches['team1'] == team1) & (matches['team2'] == team2)) |
              ((matches['team1'] == team2) & (matches['team2'] == team1))]
h2h_result = h2h['winner'].value_counts()
st.dataframe(h2h[['season', 'date', 'winner', 'venue']])
fig9 = px.bar(h2h_result, x=h2h_result.index, y=h2h_result.values, labels={'x': 'Team', 'y': 'Wins'}, color=h2h_result.index)
st.plotly_chart(fig9)

# --- Player Stats Search ---
st.markdown("## 🔍 Player Stats Search")

# Get all unique players
all_batters = deliveries['batter'].unique()
all_bowlers = deliveries['bowler'].unique()
all_players = sorted(set(all_batters).union(set(all_bowlers)))

selected_player = st.selectbox("Select Player", all_players)

if selected_player:
    st.markdown(f"### 📄 Stats for: `{selected_player}`")

    # Batting stats
    player_batting = deliveries[deliveries['batter'] == selected_player]
    total_runs = player_batting['batsman_runs'].sum()
    balls_faced = player_batting.shape[0]
    strike_rate = (total_runs / balls_faced) * 100 if balls_faced > 0 else 0
    total_fours = player_batting[player_batting['batsman_runs'] == 4].shape[0]
    total_sixes = player_batting[player_batting['batsman_runs'] == 6].shape[0]

    # Bowling stats
    player_bowling = deliveries[deliveries['bowler'] == selected_player]
    total_balls_bowled = player_bowling.shape[0]
    total_runs_conceded = player_bowling['total_runs'].sum()
    wickets = player_bowling[player_bowling['dismissal_kind'].isin(valid_dismissals)].shape[0]

    # Matches played
    matches_played = pd.concat([player_batting, player_bowling])['match_id'].nunique()

    # Display metrics
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.metric("🏏 Total Runs", f"{total_runs}")
        st.metric("🎯 Total Wickets", f"{wickets}")
    with col_p2:
        st.metric("⚾ Balls Faced", f"{balls_faced}")
        st.metric("📊 Strike Rate", f"{strike_rate:.2f}")
    with col_p3:
        st.metric("🔨 4s / 6s", f"{total_fours} / {total_sixes}")
        st.metric("📅 Matches Played", f"{matches_played}")

# --- Team Comparison Tool ---
st.markdown("## 🆚 Team Comparison Tool")

team_a = st.selectbox("Select Team A", sorted(matches['team1'].dropna().unique()), key='team_a')
team_b = st.selectbox("Select Team B", sorted(matches['team2'].dropna().unique()), key='team_b')

if team_a != team_b:
    col_t1, col_t2 = st.columns(2)

    def team_stats(team):
        team_matches = matches[(matches['team1'] == team) | (matches['team2'] == team)]
        total = team_matches.shape[0]
        wins = team_matches[team_matches['winner'] == team].shape[0]
        win_pct = (wins / total * 100) if total else 0

        team_batting = deliveries[deliveries['batting_team'] == team]
        team_bowling = deliveries[deliveries['bowling_team'] == team]

        total_runs = team_batting['total_runs'].sum()
        total_wickets = team_bowling[team_bowling['dismissal_kind'].isin(valid_dismissals)].shape[0]

        avg_runs = total_runs / total if total else 0
        avg_wickets = total_wickets / total if total else 0

        top_batter = team_batting.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(1)
        top_bowler = team_bowling[team_bowling['dismissal_kind'].isin(valid_dismissals)] \
                     .groupby('bowler').size().sort_values(ascending=False).head(1)

        return wins, win_pct, avg_runs, avg_wickets, top_batter, top_bowler

    # Team A metrics
    wins_a, pct_a, avg_runs_a, avg_wkt_a, top_bat_a, top_bowl_a = team_stats(team_a)
    with col_t1:
        st.markdown(f"### 🟡 {team_a}")
        st.metric("🏆 Total Wins", wins_a)
        st.metric("📊 Win %", f"{pct_a:.2f}%")
        st.metric("🏏 Avg Runs/Match", f"{avg_runs_a:.1f}")
        st.metric("🎯 Avg Wickets/Match", f"{avg_wkt_a:.1f}")
        if not top_bat_a.empty:
            st.metric("🥇 Top Batter", f"{top_bat_a.index[0]} ({top_bat_a.iloc[0]} runs)")
        if not top_bowl_a.empty:
            st.metric("🥇 Top Bowler", f"{top_bowl_a.index[0]} ({top_bowl_a.iloc[0]} wickets)")

    # Team B metrics
    wins_b, pct_b, avg_runs_b, avg_wkt_b, top_bat_b, top_bowl_b = team_stats(team_b)
    with col_t2:
        st.markdown(f"### 🔵 {team_b}")
        st.metric("🏆 Total Wins", wins_b)
        st.metric("📊 Win %", f"{pct_b:.2f}%")
        st.metric("🏏 Avg Runs/Match", f"{avg_runs_b:.1f}")
        st.metric("🎯 Avg Wickets/Match", f"{avg_wkt_b:.1f}")
        if not top_bat_b.empty:
            st.metric("🥇 Top Batter", f"{top_bat_b.index[0]} ({top_bat_b.iloc[0]} runs)")
        if not top_bowl_b.empty:
            st.metric("🥇 Top Bowler", f"{top_bowl_b.index[0]} ({top_bowl_b.iloc[0]} wickets)")

    # Head-to-head
    h2h_matches = matches[((matches['team1'] == team_a) & (matches['team2'] == team_b)) |
                          ((matches['team1'] == team_b) & (matches['team2'] == team_a))]
    h2h_wins = h2h_matches['winner'].value_counts()

    st.markdown("### 🤝 Head-to-Head Results")
    fig_h2h = px.bar(h2h_wins, x=h2h_wins.index, y=h2h_wins.values,
                     labels={'x': 'Team', 'y': 'Wins'}, color=h2h_wins.index)
    st.plotly_chart(fig_h2h, use_container_width=True, key='h2h_chart')


# --- Venue Analysis ---
st.markdown("## 🏟️ Venue Analysis")

venue_counts = matches['venue'].value_counts().reset_index()
venue_counts.columns = ['Venue', 'Matches']
fig_venue = px.bar(venue_counts, x='Venue', y='Matches', title='Matches Played at Each Venue', color='Venue')
st.plotly_chart(fig_venue)

st.markdown("### 📍 Team Win % by Venue")
team_venue = st.selectbox("Select Team", sorted(matches['team1'].dropna().unique()), key='venue_team')
venue_filtered = matches[(matches['team1'] == team_venue) | (matches['team2'] == team_venue)]

venue_stats = venue_filtered.groupby('venue').agg(
    total_matches=('id', 'count'),
    wins=('winner', lambda x: (x == team_venue).sum())
).reset_index()

venue_stats['win_pct'] = (venue_stats['wins'] / venue_stats['total_matches']) * 100
venue_stats = venue_stats.sort_values(by='win_pct', ascending=False)

fig_team_venue = px.bar(venue_stats, x='venue', y='win_pct',
                        title=f"{team_venue} Win % at Venues", color='venue')
st.plotly_chart(fig_team_venue)

# --- Player vs Player ---
st.markdown("## ⚔️ Player vs Player (Batter vs Bowler)")

batter_list = sorted(deliveries['batter'].unique())
bowler_list = sorted(deliveries['bowler'].unique())

col_pvp1, col_pvp2 = st.columns(2)
with col_pvp1:
    selected_batter = st.selectbox("Select Batter", batter_list)
with col_pvp2:
    selected_bowler = st.selectbox("Select Bowler", bowler_list)

pvp = deliveries[(deliveries['batter'] == selected_batter) & (deliveries['bowler'] == selected_bowler)]

balls = pvp.shape[0]
runs = pvp['batsman_runs'].sum()
fours = pvp[pvp['batsman_runs'] == 4].shape[0]
sixes = pvp[pvp['batsman_runs'] == 6].shape[0]
dismissals = pvp[pvp['dismissal_kind'].isin(valid_dismissals)].shape[0]
strike_rate = (runs / balls * 100) if balls > 0 else 0

st.markdown(f"### 📊 {selected_batter} vs {selected_bowler}")
col_pvp3, col_pvp4, col_pvp5 = st.columns(3)
col_pvp3.metric("Balls Faced", balls)
col_pvp4.metric("Runs Scored", runs)
col_pvp5.metric("Strike Rate", f"{strike_rate:.2f}")

col_pvp6, col_pvp7, col_pvp8 = st.columns(3)
col_pvp6.metric("4s", fours)
col_pvp7.metric("6s", sixes)
col_pvp8.metric("Dismissals", dismissals)

