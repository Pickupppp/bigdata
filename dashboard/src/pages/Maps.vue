<template>
  <div class="content">
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      >
        <md-card>
          <md-card-header data-background-color="orange">
            <h4 class="title">发帖 ip 地图</h4>
            <p class="category">最近更新 24 小时</p>
          </md-card-header>
          <md-card-content>
            <div
              id="chinaMap"
              :style="{ width: '100%', height: '600px' }"
            ></div>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import "@/static/js/china.js";

export default {
  data() {
    return {
      ip: [],
    };
  },
  methods: {
    initEchartMap() {
      let mapDiv = document.getElementById("chinaMap");
      let myChart = this.$echarts.init(mapDiv);
      let options = {
        tooltip: {
          triggerOn: "mousemove", //mousemove、click
          padding: 8,
          borderWidth: 1,
          borderColor: "#409eff",
          backgroundColor: "rgba(255,255,255,0.7)",
          textStyle: {
            color: "#000000",
            fontSize: 13,
          },
          formatter: function (e, t, n) {
            let data = e.data;
            let context = `
               <div>
                   <p><b style="font-size:15px;">${data.name}</b></p>
                   <p class="tooltip_style"><span class="tooltip_left">发帖数量</span><span class="tooltip_right">${data.value}</span></p>
               </div>
            `;
            return context;
          },
        },
        visualMap: {
          show: true,
          left: 26,
          bottom: 40,
          showLabel: true,
          pieces: [
            {
              gte: 100,
              label: ">= 100",
              color: "#1f307b",
            },
            {
              gte: 50,
              lt: 100,
              label: "50 - 100",
              color: "#6f83db",
            },
            {
              gte: 10,
              lt: 50,
              label: "10 - 50",
              color: "#9face7",
            },
            {
              lt: 10,
              label: "<10",
              color: "#bcc5ee",
            },
          ],
        },
        geo: {
          map: "china",
          scaleLimit: {
            min: 1,
            max: 2,
          },
          zoom: 1,
          top: 120,
          label: {
            normal: {
              show: true,
              fontSize: "14",
              color: "rgba(0,0,0,0.7)",
            },
          },
          itemStyle: {
            normal: {
              borderColor: "rgba(0, 0, 0, 0.2)",
            },
            emphasis: {
              areaColor: "#f2d5ad",
              shadowOffsetX: 0,
              shadowOffsetY: 0,
              borderWidth: 0,
            },
          },
        },
        series: [
          {
            name: "突发事件",
            type: "map",
            geoIndex: 0,
            data: [],
          },
        ],
      };
      myChart.showLoading();
      this.$axios.get("http://123.249.35.243:5000/post/ip").then((res) => {
        console.log(res.data.data);
        this.ip = res.data.data;
        options.series[0].data = this.ip;
        myChart.setOption(options);
        myChart.hideLoading();
      });
    },
  },
  mounted() {
    this.initEchartMap();
  },
};
</script>
