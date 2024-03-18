<template>
        <div id="laptop" class="container product-cards p-0 mt-0">
            <!-- <div id="toast"></div> -->
            <div class="product-owl-carousel owl-carousel">
                <div v-for="item in same_product" :key="item._id" class="card">
                    <a :href="'/store/' + item._id">
                        <div class="home-product-item__favourite">
                            <span>Giảm {{ item.discount }}%</span>
                        </div>
                        <img :src="item.img" alt="">
                        <div class="card-body">
                            <h3 class="item-name">{{ item.name }}</h3>
                            <p class="item-description">{{ item.description }}</p>
                            <h5 style="font-weight: 700;">
                            {{ formatCurrency(item.price) }}
                            <span>
                                <a @click="addToFavour($event, item._id)"><i class="fa-solid fa-heart"></i></a>
                            </span>
                            </h5>
                        </div>
                    </a>
                </div>
            </div>
        </div>
</template>

<script> 
import { showSuccessToast, showWarnToast, formatCurrency, owlCarousel } from "../../../assets/web/js/main";
import productApi from '../../../service/Product';
import favourApi from '../../../service/favour';

export default {
    props:{
        same: String
    },
    data() {
        return {
            cart: {
                productId: '',
                num: '',
            },
            same_product: [],
        }
    },
    methods: {
        formatCurrency,
        async getSameProduct() {
            const res = await productApi.getSameProduct();
            this.same_product = res.data;
        },
        async addToFavour(e, id) {
            e.preventDefault();
            if (sessionStorage.getItem("login")) {
                const res = await favourApi.addToFavour(id)
                if (res.responseCode == 1)
                showSuccessToast('Đã thêm sản phẩm vào yêu thích !!')

                if (res.responseCode == 2)
                showWarnToast('Sản phẩm đã có trong yêu thích !!')
            } else {
                sessionStorage.setItem("err", true)
                this.$router.push("/auth/sign-in")
            }
        },
    },
    mounted() {
        this.getSameProduct();
    },
    updated() {
        owlCarousel(".product-owl-carousel")
    },
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

.card:hover .home-product-item__favourite {
  opacity: 1;
}
</style>