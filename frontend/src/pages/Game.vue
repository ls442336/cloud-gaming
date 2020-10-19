<template>
  <q-page>
    <div class="page-body">
      <div class="container">
        <div class="col-6 full-width full-height">
          <canvas id="canvas" class="canvas" />
          <div
            class="game-bgimage"
            :style="{ backgroundImage: `url(${game.background_url})` }"
            id="gsp_info_screen"
          >
            <div class="absolute-full loading-bg">
              <div></div>
              <div class="loading">
                <q-spinner-dots class="dots" />
              </div>
              <div class="info" id="gsp_client_info"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { createNamespacedHelpers } from "vuex";
const { mapState, mapActions } = createNamespacedHelpers("games");
import StreamRenderer from "../gsp_client/StreamRenderer";
import GspClient from "../gsp_client/GspClient";

export default {
  name: "Game",
  computed: {
    ...mapState(["game"])
  },
  methods: {
    ...mapActions(["findGameById"])
  },
  created() {
    this.findGameById(this.$route.params.id);
  },
  mounted() {
    this.streamRenderer = new StreamRenderer("canvas");
    this.streamRenderer.start();
    this.gspClient = new GspClient(
      this.$route.params.id,
      this.streamRenderer,
      "gsp_client_info",
      "gsp_info_screen"
    );
    this.gspClient.connect("localhost", 9000);
  }
};
</script>

<style lang="stylus" scoped>
.page-body
  margin 0

  .loading
    color: white;

  .info {
    width: 100%;
    text-align: center;
    position: absolute;
    color: white;
    font-size: 2.6rem;
    text-align: center;
    font-weight: 300;
    font-family: Roboto;
    bottom: 4.16rem;
    padding: 0;
  }

  .dots {
    font-size: 8rem;
  }

  .loading-bg
    display: flex;
    flex-flow: column;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.7);

  .game-bgimage {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
  }

  .canvas {
    position: absolute;
    top: 0;
    left: 0;
  }
</style>
