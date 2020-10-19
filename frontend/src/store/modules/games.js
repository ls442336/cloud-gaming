import { gameService } from '../../services'

const state = {
  games: [],
  popularGames: [],
  game: {},
  isFetchingGames: false,
  isFetchingPopularGames: false
};

const mutations = {
  setGames(state, payload) {
    state.games = payload
  },
  setGame(state, payload) {
    state.game = payload
  },
  setPopularGames(state, payload) {
    state.popularGames = payload
  },
  clearGames(state, payload) {
    state.games = []
  },
  setFetchingGames(state, payload) {
    state.isFetchingGames = payload
  },
  setFetchingPopularGames(state, payload) {
    state.isFetchingPopularGames = payload
  }
};

const actions = {
  async loadGames({ commit }) {
    commit('setFetchingGames', true)
    const { data: { docs: games } } = await gameService.getAll();
    commit('setFetchingGames', false)
    commit('setGames', games);
  },
  async findGameById({ commit }, payload) {
    const { data: game } = await gameService.getById(payload);
    commit('setGame', game);
  },
  async loadPopularGames({ commit }, payload) {
    commit('setFetchingPopularGames', true)
    const { data } = await gameService.getMostPopular(payload)
    commit('setPopularGames', data)
    commit('setFetchingPopularGames', false)
  },
  async search({commit}, payload) {
    commit('setFetchingGames', true)
    const { data: { docs: games } } = await gameService.search(payload);
    commit('setFetchingGames', false)
    commit('setGames', games)
  },
  async clearGames({commit}) {
    commit('clearGames', [])
  },
};

const getters = {};

export default {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
