
<template>
  <section class="product-detail">
    <div id="toast">
    </div>
    <div class="container">
      <div class="row">
        <div class="breadcrumbs d-flex flex-row align-items-center col-12">
          <ul>
            <li><a href="/home">Trang chủ</a></li>
            <li><a href="/store"><i class="fa fa-angle-right" aria-hidden="true"></i>Cửa hàng</a></li>
            <li class="active"><a href="#"><i class="fa fa-angle-right" aria-hidden="true"></i>Sản phẩm</a></li>
          </ul>
        </div>
        <div class="col-md-5 order-2 order-md-1">
          <img :src="product.img" alt="">
        </div>
        <div class="col-md-7 order-1 order-md-2">
          <h1>{{ product.name }}</h1>
          <div class="pd-rating mb-2">
            <i class="fa fa-star checked"></i>
            <i class="fa fa-star checked"></i> 
            <i class="fa fa-star checked"></i>
            <i class="fa fa-star checked"></i>
            <i class="fa fa-star checked"></i>
          </div>
          <div v-for="item in product.description.split(';')" :key="item">
            <p>{{ item }}</p>
          </div>
          <h5>
            Giảm giá: {{ product.discount }}%
          </h5>
          <h3>
            Giá: {{ formatCurrency(product.price - (product.price * product.discount / 100)) }}
            <del v-if="product.discount > 0">{{ formatCurrency(product.price) }}</del>
          </h3>
          
          <label for="" >Tình trạng: <span v-if="product.quantity > 0"><strong>Còn hàng</strong></span> <span v-else><strong>Hết hàng</strong></span></label>
          <form @submit.prevent="addToCart()">
            <input name="productId" :value="product._id" hidden>
            <div class="quantity">
              <div class="pro-qty">
                <span @click="decFunction(1)" class="dec qtybtn">-</span>
                <input v-if="!cart.num" class="id-1" id="quanty" type="text" value="1" name="numProduct">
                <input v-else class="id-1" id="quanty" type="text" :value="cart.num" name="numProduct">
                <span @click="cart.num < product.quantity ? incFunction(1) : null" class="inc qtybtn">+</span>
              </div>
              <a><button class="primary-btn pd-cart" type="submit">Thêm vào giỏ hàng</button></a>
              <a class="favour-container"><button class="favour-btn" @click="addToFavour($event,product._id)"><i class="fa-solid fa-heart"></i></button></a>
            </div>
          </form>
        </div>
      </div>
      <div>
        <span class="same-product">SẢN PHẨM TƯƠNG TỰ</span>
        <productSame :same="product.categoryName" v-if="isProductLoaded"/>
      </div>
    </div>
  </section>
</template>

<script>
import { decFunction, incFunction, showSuccessToast, showErrorToastMess, showWarnToast, formatCurrency, owlCarousel } from "../../../assets/web/js/main";
import productApi from "../../../service/Product";
import cartApi from "../../../service/Cart";
import favourApi from "../../../service/favour";
import productSame from "./same-product.vue"
export default {
  components:{
    productSame
  },
  data() {
    return {
      product: {
        name: '',
        img: '',
        description: '',
        price: 0,
        discount: 0,
        id: ''
      },
      cart: {
        productId: "",
        num:1
      },
      isProductLoaded: false 
    };
  },
  methods: {
    formatCurrency,
    decFunction(num) {
      this.cart.num = decFunction(num);
    },
    incFunction(num) {
      this.cart.num = incFunction(num)
    },

    async addToCart(){
      try{
        if(sessionStorage.getItem("login"))
        {
          this.cart.productId=this.product._id
          await cartApi.addToCart(this.cart)
          showSuccessToast('Thêm vào giỏ hàng thành công')
        }
        else{
          sessionStorage.setItem("err",true)
          this.$router.push("/auth/sign-in")
        }
      }catch(err){
        showErrorToastMess('Sản phẩm đang hết hàng bạn nhé !! Vui lòng chọn sản phẩm khác')
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
    async getProductbyId(id){
      try{
        const res = await productApi.getProductById(id)
        this.product = res.data
        this.isProductLoaded = true; 
        console.log("vao !!")
      }
      catch(err) {
        console.log("err: " + err)
      }
    },
  },
  mounted() {
    this.getProductbyId(this.$route.params.id);
  },
  watch(){
    decFunction(num) 
    incFunction(num)
    
  }
};
</script>

<style>
.same-product{
  font-size: 24px;
  font-weight: 700;
}
</style>