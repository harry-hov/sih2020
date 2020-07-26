import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Server Logs | Dashboard',
      theme: ThemeData(
        primarySwatch: Colors.teal,
      ),
      home: MyHomePage(title: 'Server Logs | Dashboard'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    int count;
    double grid1, grid2;
    final List<Data> chartData = [
            Data("2018-01-13 01:00", 35),
            Data("2018-01-14 01:00", 10),
            Data("2018-01-15 01:00", 34),
            Data("2018-01-16 01:00", 32),
            Data("2018-01-17 01:00", 50),
            Data("2018-01-18 01:00", 70),
            Data("2018-01-19 01:00", 30),
            Data("2018-01-20 01:00", 100),
            Data("2018-01-21 01:00", 30),
            Data("2018-01-22 01:00", 29),
        ];
    if (MediaQuery.of(context).orientation == Orientation.landscape) {
      count = 2;
      grid1 = 2.9;
      grid2 = 1.8;
    }
    else {
      count = 1;
      grid1 = 1.8;
      grid2 = 2.3;
    }
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      drawer: Drawer(
        child: ListView(
          children: <Widget>[
            ListTile(
              leading: Icon(Icons.home),
              title: Text("Home"),
            ),
            ListTile(
              leading: Icon(Icons.call_to_action),
              title: Text("Stats"),
            ),
            ListTile(
              leading: Icon(Icons.info),
              title: Text("About"),
            ),
          ],
        ),
      ),
      body: 
            
      SingleChildScrollView(
        child: Column(
          children: <Widget>[
            Container(
              height: 10,
            ),
            Container(
              child: GridView.count(
                primary: false,
                crossAxisCount: 1,
                padding: const EdgeInsets.all(10.0),
                childAspectRatio: grid1,
                mainAxisSpacing: 2.0,
                crossAxisSpacing: 2.0,
                children: <Widget>[
                  Container(
                    child: Card(
                      elevation:4,
                      margin: EdgeInsets.fromLTRB(8.0, 8.0, 8.0, 8.0),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      color: Colors.white,  
                      child: Container(
                        padding: EdgeInsets.fromLTRB(30.0,20.0,50.0,30.0),
                        child: SfCartesianChart(
                          title: ChartTitle(text: 'Real-Time Log Graph',backgroundColor: Colors.blueGrey[100]),
                          enableAxisAnimation: true,
                          crosshairBehavior: CrosshairBehavior(enable:true),
                          tooltipBehavior: TooltipBehavior(enable: true),
                          zoomPanBehavior: ZoomPanBehavior(
                            enableDoubleTapZooming: true,
                          ),
                          borderColor: Colors.black,
                          borderWidth: 2,
                          primaryXAxis: CategoryAxis(
                            edgeLabelPlacement: EdgeLabelPlacement.shift,
                            majorTickLines: MajorTickLines(
                              color: Colors.black
                            ),
                          ),
                          primaryYAxis: NumericAxis(
                            majorTickLines: MajorTickLines(
                               color: Colors.black
                             ),
                            title: AxisTitle(
                                text: 'Number of HTTP requests',
                                textStyle: TextStyle (
                                  fontWeight: FontWeight.w700
                                )
                            )
                          ),
                          series: <ChartSeries>[
                            FastLineSeries<Data,String>(
                                dataSource: chartData,
                                xValueMapper: (Data sales, _) => sales.date,
                                yValueMapper: (Data sales, _) => sales.reqNo,
                                animationDuration: 1000,
                                markerSettings: MarkerSettings(
                                    isVisible: true
                                )
                            )
                          ]
                        )
                      )
                    ),
                  ),
                ],
                shrinkWrap: true,
              )
            ),
            Container(
              height: 10,
            ),
            Container(
              child: GridView.count(
                primary: false,
                crossAxisCount: count,
                padding: const EdgeInsets.all(10.0),
                childAspectRatio: grid2,
                mainAxisSpacing: 2.0,
                crossAxisSpacing: 5.0,
                children: List.generate(20, (index) {
                  return Container(
                    child: Card(
                      elevation: 4,
                      margin: EdgeInsets.fromLTRB(8.0, 8.0, 8.0, 8.0),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      color: Colors.white,
                    ),
                  );
                }),
                shrinkWrap: true,
              ),
            ),
            Container(
              height: 30,
            ),
            Container(
              child: Center(
                child: Text(
                  "© permission_denied",
                  style: TextStyle(
                    color: Colors.grey[800],
                    fontWeight: FontWeight.w100,
                    fontSize: 12,
                  ),
                ),
              ),
            ),
            Container(
              height: 20,
            ),
          ],
        ),
      ),
    );
  }
}

class Data {
  Data(this.date, this.reqNo);
    final String date;
    final double reqNo;
}
