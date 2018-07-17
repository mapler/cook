var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};
option = null;

function addData() {
    $.ajax({url: host + '/device/' + deviceId + '/channels/' + channelId + '/real_time/data/', context: data}).done(function (res){
        var value = res.value;
        data.push(value);
        var now = new Date().toLocaleTimeString();
        time.push(now);
    });

    if (data.length > slices) {
        time.shift();
        data.shift();
    };
}


option = {
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: time
    },
    yAxis: {
        boundaryGap: [0, '50%'],
        type: 'value'
    },
    series: [
        {
            name:'channel',
            type:'line',
            lineStyle:{
              normal: {
                color: '#18bc9c',
                width: 4,
              }
            },
            animation: true,
            smooth:true,
            showSymbol: false,
            data: data
        }
    ]
};

app.timeTicket = setInterval(function () {
    addData();
    myChart.setOption({
        xAxis: {
            data: time
        },
        series: [{
            name:'channel',
            data: data
        }]
    });
}, duration/slices*1000);

if (option && typeof option === "object") {
    myChart.setOption(option, true);
}