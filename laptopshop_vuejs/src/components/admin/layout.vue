<style>
@import url(https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css);
@import url(https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css);
@import url(../../assets/admin/css/style.css);
@import url(../../assets/admin/css/adminlte.min.css);
@import url(../../assets/web/css/toast.css);
@import url(../../assets/web/css/pagination.css);
</style>

<script >
import Header from './shared/header.vue';
import Footer from './shared/footer.vue';
import Menu from './shared/menu.vue';
import Backtotop from './shared/back-to-top.vue';
import '../../assets/admin/js/jquery.min.js'
// import '../../assets/admin/js/adminlte.min.js'
import '../../assets/admin/js/back-to-top.js'

export default{

  components: {
    Header,
    Footer,
    Menu,
    Backtotop,
  }
}
</script>

<template>
  <div>
    <Header />
    <Menu />

    <!-- Ở đây cần import content  -->
    <div class="content-wrapper">
      <router-view></router-view>
    </div>

    <Backtotop />
    
    <Footer />
  </div>
</template>

