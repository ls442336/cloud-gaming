<template>
  <q-page class="flex column page-body">
  <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          <router-link to="/" class="title"> Cloud Gaming Platform </router-link>
        </q-toolbar-title>

        <q-space />

        <q-input dark dense standout input-class="text-left" class="q-ml-md" v-model="text">
          <template v-slot:append>
            <q-icon v-if="text === ''" name="search" />
            <q-icon v-else name="clear" class="cursor-pointer" @click="text = ''" />
          </template>
        </q-input>
      </q-toolbar>
    </q-header>

    <div v-if="text === ''">
      <header class="section">
        <div class="section-title">
          Mais Populares
        </div>
      </header>

      <div class="section-title" v-if="isFetchingPopularGames">
        Carregando...
      </div>

      <div class="section-title" v-if="!isFetchingPopularGames && popularGames.length === 0">
        Nenhum resultado encontrado
      </div>

      
      <div class="gallery">
        <div class="gallery-grid">
            <card-game
              @play="playGame(item._id)"
              :imgPath="item.game.thumbnail_url"
              :key="item._id"
              v-for="(item) in popularGames"
            />
          </div>
      </div>
      

      <header class="section">
        <div class="section-title">
          Biblioteca
        </div>
      </header>

      <div class="section-title" v-if="isFetchingGames">
        Carregando...
      </div>

      <div class="section-title" v-if="!isFetchingGames && games.length === 0">
        Nenhum resultado encontrado
      </div>

      <div class="gallery">
        <div class="gallery-grid">
            <card-game
              @play="playGame(item._id)"
              :imgPath="item.thumbnail_url"
              :key="item._id"
              v-for="(item) in games"
            />
          </div>
      </div>
    </div>
    <div v-else>
      <header class="section">
        <div class="section-title">
          Resultados
        </div>
      </header>
      <div class="section-title" v-if="isLoading || isFetchingGames">
        Carregando...
      </div>
      <div class="section-title" v-if="!isLoading && games.length === 0">
        Nenhum resultado encontrado
      </div>
      <div class="gallery">
        <div class="gallery-grid">
            <card-game
              @play="playGame(item._id)"
              :imgPath="item.thumbnail_url"
              :key="item._id"
              v-for="(item) in games"
            />
          </div>
      </div>
    </div>

  </q-page>
</template>

<script>
import { createNamespacedHelpers } from "vuex";
const { mapState, mapActions } = createNamespacedHelpers("games");

import { CardGame } from './components';

export default {
  name: 'Home',
  data() {
    return {
      text: '',
      isTyping: false,
      isLoading: false
    };
  },
  watch: {
    text: function(value) {
      if(value === '') {
        this.loadGames()
        this.loadPopularGames({
          limit: 4
        })
      } else {
          this.clearGames()
          if(!this.isLoading) {
            setTimeout(() => {
              this.isLoading = false;
              this.query(this.text)
            }, 1000)
          }
        this.isLoading = true;
      }
    }
    },
  components: {
    CardGame,
  },
  computed: {
    ...mapState(['games', 'popularGames', 'isFetchingGames', 'isFetchingPopularGames'])
  },
  methods: {
    ...mapActions(['loadGames', 'loadPopularGames', 'search', 'clearGames']),
    playGame(id) {
      this.$router.push(`game/${id}`);
    },
    query(text) {
      this.search(text)
    }
  },
  created() {
    this.loadGames()
    this.loadPopularGames({
      limit: 4
    })
  }
};
</script>

<style lang="stylus" scoped>
.page-body
  padding: 3.36rem 2.56rem;

.gallery {
  margin-bottom: 3.36rem;
}

.gallery-grid {
  display: flex;
  flex-flow: column;

  @media (min-width: 768px) {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.25rem;
    margin: 0;
  }

  @media (min-width: 1024px) {
    grid-template-columns: repeat(3, 1fr);
  }

  @media (min-width: 1280px) {
    grid-template-columns: repeat(5, 1fr);
  }


  @media (min-width: 1440px) {
    grid-template-columns: repeat(5, 1fr);
  }

  @media (min-width: 2560px) {
    grid-template-columns: repeat(7, 1fr);
  }
}

.section-title
    margin: 0;
    padding: 0;
    font-weight: 300
    line-height: 3rem;
    font-size: 2.56rem;

.section {
  margin-bottom: 1.92rem;
}

.games-list {
    width: 100%;
    margin-bottom: 1.76rem;
    background-color: red;
}

.q-toolbar
  background-color #263238
  height: 5.44rem;

  a
    text-decoration none
    color #ccc
  
  .title {
    color: white;
    font-size: 1.92rem;
    text-transform: uppercase;
    font-weight: 700;
  }
</style>
