link = "https://github.com/WildCodeSchool/wilddata/raw/main/wine_df.zip"
df = pd.read_csv(link)

bouteille_df = pd.read_csv("https://raw.githubusercontent.com/WildCodeSchool/wilddata/main/domaine_des_croix_df.csv")

# Import des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import types

def main():
    # Chargement des données (avec une fonction de hachage personnalisée)
    @st.cache_data(hash_funcs={types.FunctionType: lambda _: None})  # Utilisez une fonction de hachage basique pour load_data
    def load_data():
        # Charger les données du jeu de données principal
        data = df
        # Charger les données de la bouteille du client
        client_data = bouteille_df
        return data, client_data


    # Récupération des données
    data, client_data = load_data()

    # Titre de l'application
    st.title("Analyse du Marché du Vin")

    # Rappel du contexte et de la problématique
    st.header("Contexte et Problématique")
    st.write("Le Domaine des Croix souhaite se lancer sur le marché américain du vin. Nous allons analyser les données pour recommander un prix compétitif.")

    # Analyse exploratoire des données
    st.header("Analyse Exploratoire des Données")

    # Répartition du nombre de vins par pays
    st.subheader("Répartition des Vins par Pays")
    country_counts = data['country'].value_counts()
    st.bar_chart(country_counts)

    # Pays avec les meilleures notes
    st.subheader("Pays avec les Meilleures Notes")
    best_rated_countries = data.groupby('country')['points'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(best_rated_countries)

    # Moyennes de notes par cépage
    st.subheader("Moyennes de Notes par Cépage")
    variety_avg_points = data.groupby('variety')['points'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(variety_avg_points)

    # Répartition par décile
    st.subheader("Répartition par Décile")
    decile = pd.qcut(data['price'], q=10, labels=False)
    fig, ax = plt.subplots()
    ax.hist(decile, bins=10, edgecolor='k')
    st.pyplot(fig)


    # NLP: Wordcloud pour les descriptions
    st.header("NLP: Wordcloud pour les Descriptions")
    wordcloud = WordCloud(width=800, height=400).generate(' '.join(data['description']))
    st.image(wordcloud.to_array())

    # Tableau de bord interactif
    st.header("Tableau de Bord Interactif")

    # Ajoutez vos éléments interactifs ici, par exemple des widgets Streamlit pour les filtres
    # Sélection du pays
    selected_country = st.selectbox("Sélectionnez un pays", data['country'].unique())

    # Sélection du cépage
    selected_variety = st.selectbox("Sélectionnez un cépage", data['variety'].unique())

    # Curseur pour le positionnement souhaité
    price_positioning = st.slider("Positionnement souhaité (en prix)", min_value=0, max_value=100, step=1, value=50)

    # Réponse à la question métier : proposition de prix
    st.header("Proposition de Prix")

    # Calculez la fourchette de prix recommandée en fonction du positionnement souhaité par le client
    def calculate_price_range(selected_country, selected_variety, price_positioning):
        # Filtrer les données en fonction des sélections de l'utilisateur
        filtered_data = data[(data['country'] == selected_country) & (data['variety'] == selected_variety)]

        # Calculer la fourchette de prix recommandée en fonction du positionnement souhaité
        min_price = filtered_data['price'].quantile(price_positioning / 100)
        max_price = filtered_data['price'].quantile((100 - price_positioning) / 100)

        return min_price, max_price

    if st.button("Calculer la Fourchette de Prix Recommandée"):
        min_price, max_price = calculate_price_range(selected_country, selected_variety, price_positioning)
        st.write(f"Fourchette de Prix Recommandée : De {min_price} à {max_price}")


    # Qualité esthétique du tableau de bord
    st.header("Qualité Esthétique du Tableau de Bord")

    # Personnalisez l'apparence de votre tableau de bord ici

    # Affichage des données du client
    st.header("Données du Client")
    st.write("Données de la bouteille du client :")
    st.write(client_data)

    # Vous pouvez ajouter d'autres sections personnalisées en fonction des besoins du client

    # Exécution de l'application
    if __name__ == '__main__':
        main()
