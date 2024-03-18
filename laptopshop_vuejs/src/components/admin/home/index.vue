<template>
  <div>
    <head>
      <title>Admin Page</title>
    </head>
    <div id="toast"></div>
    <section class="content-header">
      <div class="container-fluid">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1>Trang chủ</h1>
          </div>
          <div class="row gy-4 mb-3">
            <!-- Congratulations card -->
            <div v-for="cardItem in cardItems" :key="cardItem.id" class="col-md-12 col-lg-3">
              <div class="card">
                <div class="card-body">
                  <div class="card-circle">
                    <i :class="`card-icon fa-solid ${cardItem.icon}`"></i>
                  </div>
                  <div class="card-content">
                    <h4 class="card-label">{{ cardItem.label }}</h4>
                    <p class="mb-2 pb-1">{{ cardItem.value }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="d-flex">
            <div class="filter-statistical">
              <select class="form-control form-select" v-model="this.selectedFilter" @change="updateSelect()">
                <option selected="selected" value="1">Thống kê theo tháng</option>
				<option value="2">Thống kê theo khoảng ngày</option>
              </select>
              <ul v-if="this.selectedFilter == 1">
                <label style="padding-top: 10px;">Thống kê doanh thu theo năm</label>
                <li v-for="year in years" :key="year" :value="year" @click="update(year)" style="cursor: pointer; width: 300px;">
                  Năm {{ year }}: {{ formatCurrency(revenueWithYear[year]) }}
                </li>
              </ul>
              <ul v-if="this.selectedFilter == 2">
                <div class="statistical">
                  <label class="statistical-from" for="startDate">Từ ngày:</label>
                  <VueDatePicker v-model="startDate" format="yyyy-MM-dd"></VueDatePicker>
                  <label class="statistical-from" for="endDate">Đến ngày:</label>
                  <VueDatePicker v-model="endDate" format="yyyy-MM-dd"></VueDatePicker>
                  <button class="statistical-btn btn btn-primary" @click="thongKe">Thống kê</button>
                </div>
              </ul>
            </div>
            <div style="width: 1000px; height: 600px;">
              <canvas id="myChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Chart from 'chart.js/auto'
import revenueApi from '../../../service/revenue';
import { showErrorToastMess } from "../../../assets/web/js/main";
import { formatDate, formatCurrency } from "../../../assets/admin/js/format-admin";

export default {
	components: {
		VueDatePicker
	},
	data() {
		return {
			selectedFilter: 1,
			years: [],
			revenue: [],
			revenueWithYear: {},
			myChart: null,
			startDate: null,
			endDate: null,
			cardItems: [
				{ id: 1, label: 'TỔNG ĐƠN', data_name: "totalOrder" , value: null, icon: 'fa-calendar' },
				{ id: 2, label: 'TỔNG SẢN PHẨM', data_name: "totalProduct" , value: null, icon: 'fa-hand-holding-dollar' },
				{ id: 3, label: 'Người dùng đăng ký', data_name: "numUser" , value: null, icon: 'fa-user' },
				{ id: 4, label: 'Đơn hàng chờ xử lý', data_name: "numOrder" , value: null, icon: 'fa-clipboard' }
			]
		}
	},
	methods: {
		formatDate,
		formatCurrency,
		async getRevenue() {
			try {
				const res = await revenueApi.getRevenue()
				this.revenue = res.data.revenue
				this.revenue.forEach(revenue => {
				if (!this.years.includes(revenue.year))
					this.years.push(revenue.year)
				})
				this.revenue.forEach(r => {
				const year = r.year;
				const totalMoney = r.total_money_month;
				if (this.revenueWithYear.hasOwnProperty(year)) {
					this.revenueWithYear[year] += totalMoney;
				} else {
					this.revenueWithYear[year] = totalMoney;
				}
				});
				this.updateChart(this.revenue, this.years[this.years.length - 1])
			} catch (err) {
				console.log("err: " + err)
			}
		},
		async getCard() {
			try {
				const res = await revenueApi.getCard()
				this.cardItems.forEach(cardItem => {
				cardItem.value = res.data[cardItem.data_name];
				});
			} catch (err) {
				console.log("err: " + err)
			}
		},
		init() {
			const ctx = document.getElementById("myChart")
			if (!ctx) {
				console.error("Không tìm thấy phần tử có ID là 'myChart'.");
				return;
			}
			const labels = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'];
			const data = {
				labels: labels,
				datasets: [{
				label: 'Tổng doanh thu',
				data: [],
				backgroundColor: [],
				borderColor: [],
				borderWidth: 1
				}]
			};
			const chart = new Chart(ctx, {
				type: 'bar',
				data: data,
			});
			Object.seal(chart)
			this.myChart = chart
			this.getRevenue(this.myChart)
			this.getCard()
		},
		updateChart(data, year) {
			const revenueData = new Array(12).fill(0);
			for (let i = 0; i < data.length; i++) {
				if (data[i] == null || data[i] === "") {
				continue;
				} else {
				if (data[i].year === year) {
					revenueData[data[i].month - 1] += data[i].total_money_month;
				}
				}
			}
			const colors = this.generateColors(this.myChart.data.labels.length);
			this.myChart.data.datasets[0].data = revenueData;
			this.myChart.data.labels = Array.from({ length: 12 }, (_, i) => `Tháng ${i + 1}`);
			this.myChart.data.datasets[0].backgroundColor = colors;
			this.myChart.update();
		},
		update(year) {
			this.updateChart(this.revenue, year)
		},
		generateColors(count) {
			const colors = [];
			for (let i = 0; i < count; i++) {
				const color = `rgb(${this.getRandomValue(0, 255)}, ${this.getRandomValue(0, 255)}, ${this.getRandomValue(0, 255)})`;
				colors.push(color);
			}
			return colors;
		},
		getRandomValue(min, max) {
			return Math.floor(Math.random() * (max - min + 1) + min);
		},
		async thongKe() {
			let start = this.formatDate(this.startDate)
			let end = this.formatDate(this.endDate)
			let data = { start, end }
			if (start > end) {
				let error = 'Ngày bắt đầu không được lớn hơn ngày kết thúc.';
				showErrorToastMess(error)
			} else {
				try {
				const res = await revenueApi.getStatistical(data)
				this.revenue = res.data.revenueDay
				this.updateChartByDay(this.revenue)
				} catch (err) {
				showErrorToastMess("loi r")
				console.log("err: " + err)
				}
			}
		},
		updateChartByDay(data) {
			const startDate = new Date(this.startDate);
			const endDate = new Date(this.endDate);
			const daysInRange = Math.floor((endDate - startDate) / (24 * 60 * 60 * 1000)) + 1;
			const labels = Array.from({ length: daysInRange }, (_, i) => {
				const date = new Date(startDate);
				date.setDate(date.getDate() + i);
				return date.toLocaleDateString();
			});
			const dataArr = Array.from({ length: daysInRange }, () => 0);
			data.forEach((item) => {
				const year = item.year;
				const month = item.month;
				const day = item.day;
				const date = new Date(year, month - 1, day);
				const dayDifference = Math.floor((date - startDate) / (24 * 60 * 60 * 1000));
				dataArr[dayDifference] = item.total_money_day;
			});
			const colors = this.generateColors(labels.length);
			this.myChart.data.datasets[0].data = dataArr;
			this.myChart.data.labels = labels;
			this.myChart.data.datasets[0].backgroundColor = colors;
			this.myChart.update();
		},
		updateSelect() {
			if (this.selectedFilter == 1) {
				this.getRevenue()
			}
			if (this.selectedFilter == 2)
				console.log("selectedFilter: " + this.selectedFilter)
		}
	},
	mounted() {
		if (!sessionStorage.getItem("login") && sessionStorage.getItem("role") !== "ROLE_ADMIN") {
		this.$router.push("/auth/sign-in")
		sessionStorage.setItem("auth", true)
		}
		if (this.selectedFilter === 1)
		this.init()
	}
}
</script>

<style>
@import url(../../../assets/admin/css/home.css);
</style>
