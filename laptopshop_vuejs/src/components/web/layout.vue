<style>
@import url(../../assets/web/css/web.css);
@import url(../../assets/web/css/toast.css);

</style>

<script >
import Header from '../web/shared/header.vue';
import Footer from '../web/shared/footer.vue';
import Menu from '../web/shared/menu.vue';
import Backtotop from '../web/shared/back-to-top.vue';
import '../../assets/web/js/main.js'
import '../../assets/web/js/show-file-image_choosed.js';

export default{
  components: {
    Header,
    Footer,
    Menu,
    Backtotop,
  },
  data() {
    return {
      headerKey: 0,
    };
  }
}
</script>

<template>
  <div>
    <Header/>
    <Menu />
    <div class="content-wrapper">
      <!-- Ở đây cần import content  -->
      <router-view></router-view>
    </div>

    <Backtotop />
    <Footer />
  </div>
</template>

