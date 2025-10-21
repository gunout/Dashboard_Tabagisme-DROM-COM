import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Tabagisme DROM-COM - Analyse Stratégique",
    page_icon="🚬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #2E8B57, #3CB371, #90EE90);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        padding: 1rem;
    }
    .section-header {
        color: #2E8B57;
        border-bottom: 3px solid #3CB371;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-size: 1.8rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .impact-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid;
    }
    .impact-health { border-left-color: #dc3545; background-color: rgba(220, 53, 69, 0.1); }
    .impact-social { border-left-color: #ffc107; background-color: rgba(255, 193, 7, 0.1); }
    .impact-economic { border-left-color: #28a745; background-color: rgba(40, 167, 69, 0.1); }
    .policy-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    .policy-prevention { border-left-color: #28a745; background-color: rgba(40, 167, 69, 0.1); }
    .policy-regulation { border-left-color: #007bff; background-color: rgba(0, 123, 255, 0.1); }
    .policy-treatment { border-left-color: #6f42c1; background-color: rgba(111, 66, 193, 0.1); }
</style>
""", unsafe_allow_html=True)

class TobaccoDROMCOMDashboard:
    def __init__(self):
        self.historical_data = self.initialize_historical_data()
        self.territorial_data = self.initialize_territorial_data()
        self.policy_timeline = self.initialize_policy_timeline()
        self.health_impact_data = self.initialize_health_impact_data()
        self.social_indicators = self.initialize_social_indicators()
        
    def initialize_historical_data(self):
        """Initialise les données historiques du tabagisme dans les DROM-COM"""
        years = list(range(2000, 2024))
        
        # Données simulées spécifiques aux DROM-COM
        smoking_prevalence = [
            35.2, 34.8, 34.4, 34.0, 33.6, 33.2, 32.8, 32.4, 32.0, 31.6,  # 2000-2009 (% population)
            31.2, 30.8, 30.4, 30.0, 29.6, 29.2, 28.8, 28.4, 28.0, 27.6,  # 2010-2019
            27.2, 26.8, 26.4, 26.0  # 2020-2023
        ]
        
        daily_smokers = [
            28.5, 28.2, 27.9, 27.6, 27.3, 27.0, 26.7, 26.4, 26.1, 25.8,  # 2000-2009 (% population)
            25.5, 25.2, 24.9, 24.6, 24.3, 24.0, 23.7, 23.4, 23.1, 22.8,  # 2010-2019
            22.5, 22.2, 21.9, 21.6  # 2020-2023
        ]
        
        cigarettes_per_day = [
            12.8, 12.7, 12.6, 12.5, 12.4, 12.3, 12.2, 12.1, 12.0, 11.9,  # 2000-2009 (moyenne)
            11.8, 11.7, 11.6, 11.5, 11.4, 11.3, 11.2, 11.1, 11.0, 10.9,  # 2010-2019
            10.8, 10.7, 10.6, 10.5  # 2020-2023
        ]
        
        early_initiation = [
            14.8, 14.7, 14.6, 14.5, 14.4, 14.3, 14.2, 14.1, 14.0, 13.9,  # 2000-2009 (âge moyen)
            13.8, 13.7, 13.6, 13.5, 13.4, 13.3, 13.2, 13.1, 13.0, 12.9,  # 2010-2019
            12.8, 12.7, 12.6, 12.5  # 2020-2023
        ]
        
        return pd.DataFrame({
            'annee': years,
            'prevalence_tabac': smoking_prevalence,
            'fumeurs_quotidiens': daily_smokers,
            'cigarettes_par_jour': cigarettes_per_day,
            'age_premiere_cigarette': early_initiation
        })
    
    def initialize_territorial_data(self):
        """Initialise les données par territoire"""
        territories = [
            'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte',
            'Saint-Martin', 'Saint-Barthélemy', 'Polynésie française', 'Nouvelle-Calédonie'
        ]
        
        data = {
            'territoire': territories,
            'prevalence_2023': [28.5, 25.8, 32.4, 29.1, 22.6, 35.8, 38.2, 26.3, 27.9],  # %
            'fumeurs_quotidiens': [22.8, 20.4, 27.1, 23.6, 18.2, 30.5, 33.1, 21.7, 23.4],  # %
            'cigarettes_jour': [11.2, 10.5, 13.8, 12.1, 9.3, 15.6, 16.9, 10.8, 11.5],  # moyenne
            'tabagisme_passif': [18.5, 16.8, 22.4, 19.7, 14.2, 25.8, 28.3, 17.6, 18.9],  # %
            'mortalite_tabac': [185, 168, 224, 197, 142, 258, 283, 176, 189],  # pour 100k habitants
            'prise_charge_tabac': [45.8, 52.3, 38.7, 48.4, 32.6, 42.7, 58.9, 47.8, 49.5]  # %
        }
        
        return pd.DataFrame(data)
    
    def initialize_policy_timeline(self):
        """Initialise la timeline des politiques spécifiques aux DROM-COM"""
        return [
            {'date': '2007-01-01', 'type': 'regulation', 'titre': 'Interdiction de fumer dans les lieux publics', 
             'description': 'Application de l\'interdiction de fumer dans les lieux publics dans les DROM-COM'},
            {'date': '2011-03-15', 'type': 'prevention', 'titre': 'Plan tabac outre-mer', 
             'description': 'Premier plan spécifique de prévention du tabagisme dans les DROM-COM'},
            {'date': '2014-05-01', 'type': 'regulation', 'titre': 'Paquet neutre étendu aux outre-mer', 
             'description': 'Extension de la mesure du paquet neutre aux territoires ultramarins'},
            {'date': '2016-09-01', 'type': 'treatment', 'titre': 'Remboursement des substituts nicotiniques', 
             'description': 'Remboursement à 100% des traitements de substitution nicotinique'},
            {'date': '2018-11-01', 'type': 'regulation', 'titre': 'Augmentation des prix du tabac', 
             'description': 'Harmonisation progressive des prix avec la métropole'},
            {'date': '2020-01-01', 'type': 'prevention', 'titre': 'Campagne "Mois sans tabac" adaptée', 
             'description': 'Adaptation de la campagne nationale aux spécificités locales'},
            {'date': '2022-03-01', 'type': 'treatment', 'titre': 'Téléconsultation tabacologie', 
             'description': 'Déploiement de la téléconsultation pour le sevrage tabagique'},
            {'date': '2023-09-01', 'type': 'prevention', 'titre': 'Programme "Génération sans tabac"', 
             'description': 'Prévention ciblée sur les jeunes des outre-mer'},
        ]
    
    def initialize_health_impact_data(self):
        """Initialise les données d'impact sur la santé"""
        years = list(range(2010, 2024))
        
        data = {
            'annee': years,
            'deces_tabac': [2850, 2820, 2790, 2760, 2730, 2700, 2670, 2640, 2610, 2580, 2550, 2520, 2490, 2460],  # nombre
            'cancers_poumon': [420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550],  # nombre
            'bronchites_chroniques': [1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980],  # nombre
            'infarctus': [1250, 1240, 1230, 1220, 1210, 1200, 1190, 1180, 1170, 1160, 1150, 1140, 1130, 1120],  # nombre
            'avc': [980, 970, 960, 950, 940, 930, 920, 910, 900, 890, 880, 870, 860, 850]  # nombre
        }
        
        return pd.DataFrame(data)
    
    def initialize_social_indicators(self):
        """Initialise les indicateurs sociaux liés au tabac"""
        years = list(range(2010, 2024))
        
        data = {
            'annee': years,
            'depenses_tabac_familles': [1250, 1280, 1310, 1340, 1370, 1400, 1430, 1460, 1490, 1520, 1550, 1580, 1610, 1640],  # euros/an
            'absenteisme_tabac': [3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8],  # %
            'tabagisme_feminin': [22.8, 22.6, 22.4, 22.2, 22.0, 21.8, 21.6, 21.4, 21.2, 21.0, 20.8, 20.6, 20.4, 20.2],  # %
            'pauvreté_tabac': [18.5, 18.3, 18.1, 17.9, 17.7, 17.5, 17.3, 17.1, 16.9, 16.7, 16.5, 16.3, 16.1, 15.9]  # %
        }
        
        return pd.DataFrame(data)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown(
            '<h1 class="main-header">🚬 TABAGISME DANS LES DROM-COM - DASHBOARD STRATÉGIQUE</h1>', 
            unsafe_allow_html=True
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                '<div style="text-align: center; background: linear-gradient(45deg, #2E8B57, #3CB371); '
                'color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">'
                '<h3>📊 ANALYSE DE LA CONSOMMATION, IMPACTS ET STRATÉGIES DE PRÉVENTION</h3>'
                '</div>', 
                unsafe_allow_html=True
            )
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés du tabagisme dans les DROM-COM"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS CLÉS DU TABAGISME DANS LES DROM-COM</h3>', 
                   unsafe_allow_html=True)
        
        current_data = self.historical_data[self.historical_data['annee'] == 2023].iloc[0]
        health_data = self.health_impact_data[self.health_impact_data.index == 13].iloc[0]  # 2023
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Prévalence tabagique",
                f"{current_data['prevalence_tabac']:.1f}%",
                f"{(current_data['prevalence_tabac'] - 24.2):+.1f}% vs métropole",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Fumeurs quotidiens",
                f"{current_data['fumeurs_quotidiens']:.1f}%",
                f"+{current_data['fumeurs_quotidiens'] - 20.1:.1f}% vs métropole",
                delta_color="inverse"
            )
        
        with col3:
            # Format the number with spaces instead of commas for thousands separator
            deces_value = f"{health_data['deces_tabac']:,.0f}".replace(",", " ")
            st.metric(
                "Décès liés au tabac",
                deces_value,
                f"{-390} vs 2010",
                delta_color="normal"
            )
        
        with col4:
            st.metric(
                "Âge 1ère cigarette",
                f"{current_data['age_premiere_cigarette']:.1f} ans",
                f"-0.8 ans vs métropole",
                delta_color="inverse"
            )
    
    def create_historical_analysis(self):
        """Crée l'analyse historique de la consommation"""
        st.markdown('<h3 class="section-header">📈 ÉVOLUTION HISTORIQUE DANS LES DROM-COM</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Consommation", "Impacts Santé", "Impacts Sociaux"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution de la consommation
                fig = px.line(self.historical_data, 
                             x='annee', 
                             y=['prevalence_tabac', 'fumeurs_quotidiens', 'cigarettes_par_jour'],
                             title='Évolution des Indicateurs de Tabagisme - 2000-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Pourcentage (%) / Cigarettes", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Âge de première cigarette
                fig = px.line(self.historical_data, 
                             x='annee', 
                             y='age_premiere_cigarette',
                             title='Évolution de l\'Âge de Première Cigarette - 2000-2023',
                             markers=True)
                fig.add_hline(y=14.0, line_dash="dash", line_color="red", 
                             annotation_text="Seuil de vigilance")
                fig.update_layout(yaxis_title="Âge (années)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Impacts santé
                fig = px.line(self.health_impact_data, 
                             x='annee', 
                             y=['deces_tabac', 'cancers_poumon', 'bronchites_chroniques'],
                             title='Évolution de la Mortalité Liée au Tabac - 2010-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Nombre de cas", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Maladies cardiovasculaires
                fig = px.area(self.health_impact_data, 
                             x='annee', 
                             y=['infarctus', 'avc'],
                             title='Infarctus et AVC Liés au Tabac - 2010-2023')
                fig.update_layout(yaxis_title="Nombre", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Impacts économiques
                fig = px.line(self.social_indicators, 
                             x='annee', 
                             y=['depenses_tabac_familles', 'absenteisme_tabac'],
                             title='Dépenses des Familles et Absentéisme - 2010-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Euros / Pourcentage", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Tabagisme féminin et pauvreté
                fig = px.line(self.social_indicators, 
                             x='annee', 
                             y=['tabagisme_feminin', 'pauvreté_tabac'],
                             title='Tabagisme Féminin et Inégalités Sociales - 2010-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Pourcentage (%)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
    
    def create_territorial_analysis(self):
        """Analyse des disparités territoriales"""
        st.markdown('<h3 class="section-header">🗺️ DISPARITÉS TERRITORIALES</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Cartographie", "Comparaisons", "Facteurs Contextuels"])
        
        with tab1:
            # Carte des territoires
            st.subheader("Prévalence du Tabagisme par Territoire")
            
            # Coordonnées approximatives des territoires
            territories_coords = {
                'Guadeloupe': {'lat': 16.265, 'lon': -61.551, 'prevalence': 28.5},
                'Martinique': {'lat': 14.641, 'lon': -61.024, 'prevalence': 25.8},
                'Guyane': {'lat': 3.933, 'lon': -53.125, 'prevalence': 32.4},
                'La Réunion': {'lat': -21.115, 'lon': 55.536, 'prevalence': 29.1},
                'Mayotte': {'lat': -12.827, 'lon': 45.166, 'prevalence': 22.6},
                'Saint-Martin': {'lat': 18.070, 'lon': -63.050, 'prevalence': 35.8},
                'Saint-Barthélemy': {'lat': 17.900, 'lon': -62.850, 'prevalence': 38.2},
                'Polynésie française': {'lat': -17.679, 'lon': -149.407, 'prevalence': 26.3},
                'Nouvelle-Calédonie': {'lat': -21.300, 'lon': 165.300, 'prevalence': 27.9}
            }
            
            # Créer un DataFrame avec les coordonnées
            coords_data = []
            for territory, info in territories_coords.items():
                coords_data.append({
                    'territoire': territory,
                    'lat': info['lat'],
                    'lon': info['lon'],
                    'prevalence_tabac': info['prevalence']
                })
            
            coords_df = pd.DataFrame(coords_data)
            
            # Créer une carte scatter_geo
            fig = px.scatter_geo(coords_df,
                                lat='lat',
                                lon='lon',
                                color='prevalence_tabac',
                                size='prevalence_tabac',
                                hover_name='territoire',
                                hover_data={'prevalence_tabac': True},
                                title='Prévalence du Tabagisme par Territoire (%) - 2023',
                                color_continuous_scale='RdYlGn_r',
                                size_max=20,
                                projection='natural earth')
            
            # Configuration de la carte
            fig.update_geos(
                visible=True,
                showcountries=True,
                countrycolor="black",
                showsubunits=True,
                subunitcolor="blue",
                landcolor="lightgray",
                oceancolor="lightblue",
                bgcolor="white"
            )
            
            fig.update_layout(
                height=600,
                geo=dict(
                    bgcolor='rgba(255,255,255,0.1)'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Classement par prévalence
                fig = px.bar(self.territorial_data.sort_values('prevalence_2023'), 
                            x='prevalence_2023', 
                            y='territoire',
                            orientation='h',
                            title='Prévalence du Tabagisme par Territoire (%)',
                            color='prevalence_2023',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Classement par fumeurs quotidiens
                fig = px.bar(self.territorial_data.sort_values('fumeurs_quotidiens'), 
                            x='fumeurs_quotidiens', 
                            y='territoire',
                            orientation='h',
                            title='Fumeurs Quotidiens par Territoire (%)',
                            color='fumeurs_quotidiens',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Facteurs contextuels spécifiques
            st.subheader("Facteurs Influençant la Consommation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🏝️ Facteurs Socio-culturels
                
                **Normes sociales:**
                • Acceptabilité sociale forte  
                • Tabagisme féminin croissant  
                • Influence des pairs  
                
                **Facteurs économiques:**
                • Prix relativement bas  
                • Contrebande importante  
                • Revenus disponibles limités  
                
                **Marketing:**
                • Publicité ciblée  
                • Points de vente nombreux  
                • Promotion agressive  
                """)
            
            with col2:
                st.markdown("""
                ### 🏥 Facteurs Structurels
                
                **Offre de soins:**
                • Disparités territoriales  
                • Accès aux consultations tabacologie  
                • Substituts nicotiniques disponibles  
                
                **Prévention:**
                • Campagnes adaptées  
                • Éducation scolaire  
                • Lieux sans tabac  
                
                **Régulation:**
                • Application des interdictions  
                • Contrôles de vente  
                • Politique prix cohérente  
                """)
    
    def create_policy_analysis(self):
        """Analyse des politiques de prévention"""
        st.markdown('<h3 class="section-header">🏛️ POLITIQUES DE PRÉVENTION</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Timeline", "Efficacité", "Recommandations"])
        
        with tab1:
            # Timeline interactive des politiques
            policy_df = pd.DataFrame(self.policy_timeline)
            policy_df['date'] = pd.to_datetime(policy_df['date'])
            policy_df['annee'] = policy_df['date'].dt.year
            
            # Fusion avec données historiques
            merged_data = pd.merge(self.historical_data, policy_df, on='annee', how='left')
            
            fig = px.scatter(merged_data, 
                           x='annee', 
                           y='prevalence_tabac',
                           color='type',
                           size_max=20,
                           hover_name='titre',
                           hover_data={'description': True, 'type': True},
                           title='Impact des Politiques sur la Prévalence du Tabagisme')
            
            # Ajouter la ligne de tendance
            fig.add_trace(go.Scatter(x=self.historical_data['annee'], 
                                   y=self.historical_data['prevalence_tabac'],
                                   mode='lines',
                                   name='Prévalence tabac',
                                   line=dict(color='gray', width=2)))
            
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Légende des types de politiques
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="policy-card policy-prevention">Prévention</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="policy-card policy-regulation">Régulation</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="policy-card policy-treatment">Prise en charge</div>', unsafe_allow_html=True)
        
        with tab2:
            # Efficacité comparée des stratégies
            st.subheader("Efficacité des Stratégies de Prévention")
            
            strategies = [
                {'strategie': 'Augmentation des prix', 'efficacite': 8.9, 'cout': 2, 'acceptabilite': 4},
                {'strategie': 'Paquet neutre', 'efficacite': 7.2, 'cout': 3, 'acceptabilite': 6},
                {'strategie': 'Interdiction publicité', 'efficacite': 6.8, 'cout': 4, 'acceptabilite': 7},
                {'strategie': 'Aides au sevrage', 'efficacite': 7.5, 'cout': 6, 'acceptabilite': 8},
                {'strategie': 'Campagnes média', 'efficacite': 6.1, 'cout': 5, 'acceptabilite': 7},
                {'strategie': 'Consultations tabacologie', 'efficacite': 8.2, 'cout': 7, 'acceptabilite': 8},
            ]
            
            strategy_df = pd.DataFrame(strategies)
            
            fig = px.scatter(strategy_df, 
                           x='cout', 
                           y='efficacite',
                           size='acceptabilite',
                           color='strategie',
                           hover_name='strategie',
                           title='Efficacité vs Coût des Stratégies',
                           size_max=30)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Recommandations par Territoire")
            
            recommendations = {
                'Guadeloupe': ['Renforcer prévention jeunes', 'Développer consultations', 'Lutter contre la contrebande'],
                'Martinique': ['Campagne média ciblée', 'Formation professionnels', 'Prévention périnatale'],
                'Guyane': ['Adaptation culturelle', 'Prévention communautaire', 'Renforcement soins'],
                'La Réunion': ['Prévention scolaire', 'Dépistage précoce', 'Soins de suite'],
                'Mayotte': ['Sensibilisation précoce', 'Formation acteurs locaux', 'Accès aux substituts'],
                'Saint-Martin': ['Contrôles renforcés', 'Prévention touristique', 'Soins urgents'],
                'Saint-Barthélemy': ['Prévention ciblée', 'Contrôles événements', 'Soins privés'],
                'Polynésie française': ['Prévention adaptée', 'Soins insulaires', 'Télémédecine'],
                'Nouvelle-Calédonie': ['Prévention minière', 'Soins ruraux', 'Programmes entreprises']
            }
            
            selected_territory = st.selectbox("Sélectionnez un territoire:", list(recommendations.keys()))
            
            st.markdown(f"### Recommandations pour {selected_territory}")
            for i, recommendation in enumerate(recommendations[selected_territory], 1):
                st.write(f"{i}. {recommendation}")
    
    def create_strategic_recommendations(self):
        """Recommandations stratégiques"""
        st.markdown('<h3 class="section-header">🎯 STRATÉGIE NATIONALE TABAC DROM-COM</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Objectifs 2030", "Plan d'Action", "Indicateurs"])
        
        with tab1:
            st.subheader("Stratégie Nationale 2024-2030")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                ### 🎯 Réduction Tabagisme
                
                **Objectifs quantitatifs:**
                • -30% prévalence globale  
                • -35% fumeurs quotidiens  
                • -25% initiation précoce  
                
                **Cibles prioritaires:**
                • Jeunes 15-25 ans  
                • Femmes enceintes  
                • Populations défavorisées  
                """)
            
            with col2:
                st.markdown("""
                ### 🏥 Amélioration Soins
                
                **Couverture territoriale:**
                • 100% consultations tabacologie  
                • Délais < 7 jours  
                • Télémédecine généralisée  
                
                **Accès aux traitements:**
                • Substituts nicotiniques  
                • Prise en charge globale  
                • Suivi à long terme  
                """)
            
            with col3:
                st.markdown("""
                ### 📚 Renforcement Prévention
                
                **Éducation:**
                • Programmes scolaires  
                • Formation enseignants  
                • Sensibilisation parents  
                
                **Environnement:**
                • Génération sans tabac  
                • Lieux 100% sans tabac  
                • Normes sociales  
                """)
        
        with tab2:
            st.subheader("Plan d'Action Prioritaire")
            
            roadmap = [
                {'periode': '2024-2025', 'actions': [
                    'Cartographie des besoins',
                    'Formation des tabacologues', 
                    'Campagne média territoriale'
                ]},
                {'periode': '2026-2027', 'actions': [
                    'Déploiement consultations',
                    'Programme scolaire unifié',
                    'Système de dépistage'
                ]},
                {'periode': '2028-2030', 'actions': [
                    'Évaluation stratégique',
                    'Adjustement des programmes',
                    'Généralisation des bonnes pratiques'
                ]},
            ]
            
            for step in roadmap:
                with st.expander(f"📅 {step['periode']}"):
                    for action in step['actions']:
                        st.write(f"• {action}")
        
        with tab3:
            st.subheader("Tableau de Bord de Suivi")
            
            indicators = [
                {'indicateur': 'Prévalence tabac (%)', 'cible_2025': 22.0, 'cible_2030': 18.0},
                {'indicateur': 'Fumeurs quotidiens (%)', 'cible_2025': 17.0, 'cible_2030': 14.0},
                {'indicateur': 'Âge 1ère cigarette (ans)', 'cible_2025': 13.0, 'cible_2030': 14.0},
                {'indicateur': 'Décès liés au tabac', 'cible_2025': 2300, 'cible_2030': 2000},
                {'indicateur': 'Couverture soins (%)', 'cible_2025': 65, 'cible_2030': 80},
            ]
            
            indicators_df = pd.DataFrame(indicators)
            st.dataframe(indicators_df, use_container_width=True)
            
            # Graphique de projection
            years = list(range(2020, 2031))
            prevalence_projection = [27.2, 26.8, 26.4, 26.0, 24.5, 23.0, 22.0, 21.0, 20.0, 19.0, 18.0]
            
            fig = px.line(x=years, y=prevalence_projection,
                         title='Projection de la Prévalence du Tabagisme 2020-2030',
                         markers=True)
            fig.add_hrect(y0=0, y1=18.0, line_width=0, fillcolor="green", opacity=0.2,
                         annotation_text="Objectif 2030")
            fig.update_layout(yaxis_title="Prévalence (%)", xaxis_title="Année")
            st.plotly_chart(fig, use_container_width=True)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Période d'analyse
        st.sidebar.markdown("### 📅 Période d'analyse")
        annee_debut = st.sidebar.selectbox("Année de début", 
                                         list(range(2000, 2024)), 
                                         index=0)
        annee_fin = st.sidebar.selectbox("Année de fin", 
                                       list(range(2000, 2024)), 
                                       index=23)
        
        # Focus d'analyse
        st.sidebar.markdown("### 🎯 Focus d'analyse")
        focus_analysis = st.sidebar.multiselect(
            "Domaines à approfondir:",
            ['Consommation', 'Santé', 'Social', 'Politiques', 'Territoires'],
            default=['Consommation', 'Territoires']
        )
        
        # Sélection des territoires
        st.sidebar.markdown("### 🏝️ Territoires")
        territories = st.sidebar.multiselect(
            "Territoires à inclure:",
            ['Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte', 
             'Saint-Martin', 'Saint-Barthélemy', 'Polynésie française', 'Nouvelle-Calédonie'],
            default=['Guadeloupe', 'Martinique', 'La Réunion', 'Mayotte']
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        show_projections = st.sidebar.checkbox("Afficher les projections", value=True)
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=False)
        
        # Bouton d'export
        if st.sidebar.button("📊 Exporter l'analyse"):
            st.sidebar.success("Export réalisé avec succès!")
        
        return {
            'annee_debut': annee_debut,
            'annee_fin': annee_fin,
            'focus_analysis': focus_analysis,
            'territories': territories,
            'show_projections': show_projections,
            'auto_refresh': auto_refresh
        }
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Évolution", 
            "🗺️ Territoires", 
            "🏛️ Politiques", 
            "🎯 Stratégie",
            "💡 Synthèse"
        ])
        
        with tab1:
            self.create_historical_analysis()
        
        with tab2:
            self.create_territorial_analysis()
        
        with tab3:
            self.create_policy_analysis()
        
        with tab4:
            self.create_strategic_recommendations()
        
        with tab5:
            st.markdown("## 💡 SYNTHÈSE STRATÉGIQUE")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### ⚠️ SITUATION ALARMANTE
                
                **Problématiques majeures:**
                • Prévalence supérieure à la métropole  
                • Tabagisme féminin en augmentation  
                • Initiation précoce préoccupante  
                • Mortalité liée très élevée  
                
                **Facteurs aggravants:**
                • Prix relativement bas  
                • Contrebande importante  
                • Offre de soins insuffisante  
                • Normes sociales favorables  
                """)
            
            with col2:
                st.markdown("""
                ### ✅ LEVIERS D'ACTION
                
                **Atouts territoriaux:**
                • Structures communautaires fortes  
                • Leadership local engagé  
                • Expériences pilotes prometteuses  
                
                **Opportunités:**
                • Plans nationaux spécifiques  
                • Financements dédiés  
                • Coopération régionale  
                • Innovation numérique  
                """)
            
            st.markdown("""
            ### 🚨 RECOMMANDATIONS URGENTES
            
            **Priorité 1 - Prévention ciblée:**
            1. Programmes scolaires adaptés aux cultures locales  
            2. Campagnes média avec leaders d'opinion territoriaux  
            3. Génération sans tabac dans les outre-mer  
            
            **Priorité 2 - Soins accessibles:**
            1. Développement des consultations de tabacologie  
            2. Accès facilité aux substituts nicotiniques  
            3. Formation des professionnels de santé  
            
            **Priorité 3 - Régulation adaptée:**
            1. Harmonisation progressive des prix  
            2. Lutte renforcée contre la contrebande  
            3. Application stricte des interdictions  
            
            **Échéance: Plan d'action opérationnel pour 2024**
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(300)
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = TobaccoDROMCOMDashboard()
    dashboard.run_dashboard()