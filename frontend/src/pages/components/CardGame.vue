<template>
  <div class="my-card" @click="playGame"  :style="{backgroundImage: `url(${imgPath})`}">
    <div class="absolute play-icon-container">
        <q-icon name="play_circle_filled" class="play-icon" />
      </div>
  </div>
</template>

<script>
export default {
  name: 'CardGame',
  props: ['imgPath'],
  methods: {
    playGame() {
      this.$emit('play');
    },
  },
};
</script>

<style lang="stylus">
@keyframes card-animation {
  0% {
    background-color: rgba(0, 0, 0, 0);
  }
  100% {
    background-color: rgba(0, 0, 0, 0.64);
  }
}

@keyframes card-scale-animation {
  0% {
    transform: scale(1);
  }
  100% {
    transform: scale(1.2);
  }
}

@keyframes card-animation-rev {
  0% {
    background-color: rgba(0, 0, 0, 0.64);
  }
  100% {
    background-color: rgba(0, 0, 0, 0);
  }
}

@keyframes card-animation-icon {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes card-animation-icon-rev {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.my-card {
  flex-grow: 1;
  //max-width: 27.52rem;
  min-height: 35rem;
  position: relative;
  background-color: #ECEFF1;
  background-size: cover;
  background-position: center;
  transform: scale(1);

  @media (min-width: 768px) {
    min-height: 20rem;
  }

  @media (min-width: 1024px) {
  }

  @media (min-width: 1280px) {
    min-height: 15rem;
  }


  @media (min-width: 1440px) {
    min-height: 20rem;
  }

  @media (min-width: 2560px) {
  }

  &:hover {
    cursor: pointer
    transform: scale(1.2);
    z-index: 2;
    box-shadow: 0 0 2px #000000;
    animation-name: card-scale-animation;
    animation-duration: .2s;

    .play-icon-container {
      animation-name: card-animation;
      animation-duration: 0.3s;
      background-color: rgba(0, 0, 0, 0.64);
    }

    .play-icon {
      animation-name: card-animation-icon;
      animation-duration: 0.3s;
      opacity: 1;
    }

  }
}

.my-card {
  margin-bottom: 0.25rem;
}

.play-icon-container {
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  animation-name: card-animation-rev;
  animation-duration: 0.3;
  background-color: rgba(0, 0, 0, 0);
}

.play-icon {
  color: #ECEFF1;
  opacity: 0;
  animation-name: card-animation-icon-rev;
  animation-duration: 0.3s;
  font-size: 70px;
}

</style>
