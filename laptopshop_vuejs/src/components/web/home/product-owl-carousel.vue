<template>
<div>

  <div id="toast"></div>

  <div id="laptop" class="container product-cards p-0 mt-0">
      <h1 class="text-center">Sản phẩm</h1>
      <div class="product-owl-carousel owl-carousel">
        <div v-for="item in laptopCategory" :key="item.id" class="card">
          <a :href="'/store/' + item._id">
            <div class="home-product-item__favourite">
                <span>Giảm {{ item.discount }}%</span>
            </div>
            <img :src="item.img" alt="">
            <div class="card-body">
              <h3 class="item-name">{{ item.name }}</h3>
              <p class="item-description">{{ item.description }}</p>
              <div class="star">
                <i class="fas fa-star checked"></i>
                <i class="fas fa-star checked"></i>
                <i class="fas fa-star checked"></i>
                <i class="fas fa-star checked"></i>
                <i class="fas fa-star checked"></i>
              </div>
              <h5 style="font-weight: 700;">
                {{ formatCurrency(item.price) }}
                <span>
                  <a :href="'/store/' + item._id"> Chi tiết <i class="fa-solid fa-eye"></i></a>
                  <!-- &emsp;
                  <a @click="addToFavour($event,item.id)"><i class="fa-solid fa-heart"></i></a>
                  &emsp;
                  <a @click="addToCart($event,item.id)"><i class="fa-solid fa-cart-shopping"></i></a> -->
                </span>
              </h5>
            </div>
          </a>
        </div>
      </div>
    </div>
</div>


</template>

<script>
import { showSuccessToast, showErrorToastMess, showWarnToast, formatCurrency, owlCarousel } from "../../../assets/web/js/main";
import productApi from '../../../service/Product';
import cartApi from '../../../service/Cart';
import favourApi from '../../../service/favour';
export default {
  data() {
    return {
      laptopCategory: [],
      cart:{
        productId:'',
        num:'',
      }
    }
  },
  methods: {
    formatCurrency,
    async getAllProduct(){
      const res = await productApi.getAllProduct();
      this.laptopCategory = res.data;
    },
    async addToCart(e,id){
      try{
        e.preventDefault();
        
        if(sessionStorage.getItem("login"))
        {
          this.cart.productId=id
          await cartApi.addToCart(this.cart)
          showSuccessToast('Thêm vào giỏ hàng thành công')
        }
        else{
          sessionStorage.setItem("err",true)
          this.$router.push("/auth/sign-in")
        }
      }catch(err){
        showErrorToastMess('Thêm vào giỏ hàng thất bại')
      }
    },
    async addToFavour(e,id){
      e.preventDefault();
      if(sessionStorage.getItem("login"))
      {
        const res = await favourApi.addToFavour(id)
        if(res.responseCode == 1) 
          showSuccessToast('Đã thêm sản phẩm vào yêu thích !!')
        
        if(res.responseCode == 2)
          showWarnToast('Sản phẩm đã có trong yêu thích !!')
      }
      else{
        sessionStorage.setItem("err",true)
        this.$router.push("/auth/sign-in")
      }
    },
  },
  mounted() {
    this.getAllProduct();
  },
  updated(){
    owlCarousel(".product-owl-carousel")
  }
}
</script>

<style>
.card {
  position: relative;
  overflow: hidden;
}

.card img {
  transition: transform 0.3s ease;
}

.card:hover img {
  transform: scale(1.1);
}

.card:hover .home-product-item__favourite{
  opacity: 1;
}
</style>