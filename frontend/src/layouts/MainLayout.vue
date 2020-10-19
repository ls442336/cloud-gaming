<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>

export default {
  name: 'MainLayout'
};
</script>

<style lang="stylus" scoped>
.q-toolbar
  background-color #263238
  padding: 1.625rem !important;

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
