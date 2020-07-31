import 'package:flutter/material.dart';
import 'package:charts_flutter/flutter.dart' as charts;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Server Logs | Dashboard',
      theme: ThemeData(
        primarySwatch: Colors.blue,
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
        backgroundColor: Colors.blue,
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
                        padding: EdgeInsets.fromLTRB(30.0,20.0,20.0,30.0),
                         child: TimeSeriesRangeAnnotationMarginChart.withSampleData(),
                      ),
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
                children: List.generate(2, (index) {
                  return Container(
                    child: Card(
                      elevation: 4,
                      margin: EdgeInsets.fromLTRB(8.0, 8.0, 8.0, 8.0),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      color: Colors.white,
                      child: Container(
                        padding: EdgeInsets.fromLTRB(30.0,20.0,20.0,30.0),
                         child: DonutAutoLabelChart.withSampleData(),
                      ),
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



class TimeSeriesRangeAnnotationMarginChart extends StatelessWidget {
  final List<charts.Series> seriesList;
  final bool animate;

  TimeSeriesRangeAnnotationMarginChart(this.seriesList, {this.animate});

  factory TimeSeriesRangeAnnotationMarginChart.withSampleData() {
    return new TimeSeriesRangeAnnotationMarginChart(
      _createSampleData(),
      animate: false,
    );
  }


  @override
  Widget build(BuildContext context) {
    return new charts.TimeSeriesChart(
      seriesList,
      animate: animate,
      defaultRenderer: new charts.LineRendererConfig(includePoints: true),
      layoutConfig: new charts.LayoutConfig(
            leftMarginSpec: new charts.MarginSpec.fixedPixel(60),
            topMarginSpec: new charts.MarginSpec.fixedPixel(20),
            rightMarginSpec: new charts.MarginSpec.fixedPixel(60),
            bottomMarginSpec: new charts.MarginSpec.fixedPixel(20)),
        behaviors: [
          new charts.RangeAnnotation([
            new charts.RangeAnnotationSegment(
                35, 65, charts.RangeAnnotationAxisType.measure,
                startLabel: 'M2 Start',
                endLabel: 'M2 End',
                labelAnchor: charts.AnnotationLabelAnchor.start,
                color: charts.MaterialPalette.gray.shade300),
          ], defaultLabelPosition: charts.AnnotationLabelPosition.margin),

          new charts.LinePointHighlighter(
            showHorizontalFollowLine:
              charts.LinePointHighlighterFollowLineType.none,
            showVerticalFollowLine:
              charts.LinePointHighlighterFollowLineType.nearest),
          new charts.SelectNearest(eventTrigger: charts.SelectionTrigger.tapAndDrag),
        
          new charts.ChartTitle('Real-Time Log Graph',
            behaviorPosition: charts.BehaviorPosition.top,
            titleOutsideJustification: charts.OutsideJustification.start,
            innerPadding: 20),
          new charts.ChartTitle('Date',
            behaviorPosition: charts.BehaviorPosition.bottom,
            titleOutsideJustification:
                charts.OutsideJustification.middleDrawArea,innerPadding: 20),
          new charts.ChartTitle('Number of HTTP requests',
            behaviorPosition: charts.BehaviorPosition.start,
            titleOutsideJustification:
                charts.OutsideJustification.middleDrawArea,outerPadding: 70),
        
        ]);
  }
  static List<charts.Series<Data, DateTime>> _createSampleData() {
    final data = [
      new Data(new DateTime(2017, 9, 19), 5),
      new Data(new DateTime(2017, 9, 26), 25),
      new Data(new DateTime(2017, 10, 3), 100),
      new Data(new DateTime(2017, 10, 10), 75),
    ];

    return [
      new charts.Series<Data, DateTime>(
        id: 'noOfReq',
       // colorFn: (_, __) => charts.MaterialPalette.black,
        domainFn: (Data noOf, _) => noOf.date,
        measureFn: (Data noOf, _) => noOf.reqNo,
        data: data,
      )
    ];
  }
}

class DonutAutoLabelChart extends StatelessWidget {
  final List<charts.Series> seriesList;
  final bool animate;

  DonutAutoLabelChart(this.seriesList, {this.animate});

  factory DonutAutoLabelChart.withSampleData() {
    return new DonutAutoLabelChart(
      _createSampleData(),
      animate: false,
    );
  }


  @override
  Widget build(BuildContext context) {
    return new charts.PieChart(seriesList,
        animate: animate,
        behaviors: [
        new charts.DatumLegend(
          position: charts.BehaviorPosition.end,
          horizontalFirst: false,
          cellPadding: new EdgeInsets.only(bottom: 4.0),
          showMeasures: true,
          legendDefaultMeasure: charts.LegendDefaultMeasure.firstValue,
          measureFormatter: (num value) {
            return value == null ? '-' : '${value}Requests';
          },
        ),
      ],
        defaultRenderer: new charts.ArcRendererConfig(
            arcWidth: 50,
            arcRendererDecorators: [new charts.ArcLabelDecorator()]));
  }
  static List<charts.Series<PieData, String>> _createSampleData() {
    final data = [
      new PieData('127.0.0.1', 190742),
      new PieData('10.0.3.78', 109933),
      new PieData('158.227.105.27', 79925),
      new PieData('10.0.11.18', 31311),
    ];

    return [
      new charts.Series<PieData, String>(
        id: 'noOfReq',
       // colorFn: (_, __) => charts.MaterialPalette.blue,
        domainFn: (PieData noOfReq, _) => noOfReq.clientIP,
        measureFn: (PieData noOfReq, _) => noOfReq.noOfReq,
        data: data,
        labelAccessorFn: (PieData row, _) => '${row.clientIP}: ${row.noOfReq}',
      )
    ];
  }
}

class Data {
  Data(this.date, this.reqNo);
    final DateTime date;
    final int reqNo;
}

class PieData {
  final String clientIP;
  final int noOfReq;
  PieData(this.clientIP, this.noOfReq);
}

