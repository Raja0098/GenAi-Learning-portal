// store.js
import { createStore } from 'vuex';
import VuexPersistence from 'vuex-persist';

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
});

const store = createStore({
  state: {
    current_user: null,
  },
  mutations: {
    setCurrentUser(state, user) {
      state.current_user = user;
    },
  },
  plugins: [vuexLocal.plugin],
});

export default store;
