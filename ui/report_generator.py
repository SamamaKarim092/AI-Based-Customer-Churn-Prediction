"""
Report Generator Module
Generates professional PDF reports from churn prediction results.
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class ChurnReportGenerator:
    """Generates PDF reports for churn prediction results."""
    
    def __init__(self, prediction_data, model_info=None, include_charts=True, include_recommendations=True):
        """
        Initialize the report generator.
        
        Args:
            prediction_data: DataFrame with prediction results
            model_info: Optional dict with model performance metrics
            include_charts: Whether to include visualizations
            include_recommendations: Whether to include recommendations
        """
        self.data = prediction_data
        self.include_charts = include_charts
        self.include_recommendations = include_recommendations
        self.model_info = model_info or {
            'name': 'XGBoost',
            'accuracy': 68.35,
            'precision': 45.20,
            'recall': 90.64,
            'f1_score': 60.32,
            'roc_auc': 84.31,
            'roi': 132000,
        }
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1f6feb'),
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#58a6ff'),
            borderPadding=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor('#8b949e')
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyTextCustom',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=colors.HexColor('#333333')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CenterText',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666')
        ))
    
    def _get_summary_stats(self):
        """Calculate summary statistics from prediction data."""
        total = len(self.data)
        high_risk = len(self.data[self.data['risk_level'] == 'HIGH'])
        moderate_risk = len(self.data[self.data['risk_level'] == 'MODERATE'])
        low_risk = len(self.data[self.data['risk_level'] == 'LOW'])
        churn_count = len(self.data[self.data['prediction'] == 'Churn'])
        stay_count = total - churn_count
        churn_rate = (churn_count / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'high_risk': high_risk,
            'moderate_risk': moderate_risk,
            'low_risk': low_risk,
            'churn_count': churn_count,
            'stay_count': stay_count,
            'churn_rate': churn_rate,
        }
    
    def _create_header(self):
        """Create report header."""
        elements = []
        
        # Title
        elements.append(Paragraph("Customer Churn Prediction Report", self.styles['ReportTitle']))
        
        # Subtitle with date
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        elements.append(Paragraph(f"Generated on {date_str}", self.styles['CenterText']))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_executive_summary(self, stats):
        """Create executive summary section."""
        elements = []
        
        elements.append(Paragraph("📊 Executive Summary", self.styles['SectionHeading']))
        
        # Summary text
        risk_text = "HIGH" if stats['high_risk'] > stats['total'] * 0.3 else "MODERATE" if stats['high_risk'] > stats['total'] * 0.15 else "LOW"
        
        summary = f"""
        This report analyzes <b>{stats['total']}</b> customers for churn risk prediction. 
        Based on our machine learning model ({self.model_info['name']}), 
        <b>{stats['churn_count']}</b> customers ({stats['churn_rate']:.1f}%) are predicted to churn.
        The overall risk level for your customer base is <b>{risk_text}</b>.
        """
        elements.append(Paragraph(summary, self.styles['BodyTextCustom']))
        elements.append(Spacer(1, 10))
        
        # Add churn pie chart if enabled
        if self.include_charts:
            elements.append(self._create_churn_pie_chart(stats))
            elements.append(Spacer(1, 15))
        
        # Key metrics table
        key_data = [
            ['Metric', 'Value', 'Status'],
            ['Total Customers', str(stats['total']), '—'],
            ['Predicted to Churn', str(stats['churn_count']), '⚠️ Needs Attention' if stats['churn_rate'] > 25 else '✓ Acceptable'],
            ['Predicted to Stay', str(stats['stay_count']), '✓'],
            ['Churn Rate', f"{stats['churn_rate']:.1f}%", '⚠️ High' if stats['churn_rate'] > 30 else '✓ Normal'],
        ]
        
        table = Table(key_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f6feb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f6f8fa')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d7de')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_risk_pie_chart(self, stats):
        """Create a pie chart for risk distribution."""
        drawing = Drawing(400, 200)
        
        pie = Pie()
        pie.x = 150
        pie.y = 25
        pie.width = 150
        pie.height = 150
        
        # Data
        pie.data = [stats['high_risk'], stats['moderate_risk'], stats['low_risk']]
        pie.labels = ['High Risk', 'Moderate', 'Low Risk']
        
        # Colors
        pie.slices[0].fillColor = colors.HexColor('#cf222e')  # Red
        pie.slices[1].fillColor = colors.HexColor('#bf8700')  # Yellow/Orange
        pie.slices[2].fillColor = colors.HexColor('#238636')  # Green
        
        # Styling
        pie.slices.strokeWidth = 2
        pie.slices.strokeColor = colors.white
        pie.sideLabels = True
        pie.simpleLabels = False
        pie.slices.fontName = 'Helvetica-Bold'
        pie.slices.fontSize = 10
        
        drawing.add(pie)
        
        # Add title
        title = String(200, 185, 'Risk Level Distribution', fontSize=12, 
                      fontName='Helvetica-Bold', fillColor=colors.HexColor('#333333'),
                      textAnchor='middle')
        drawing.add(title)
        
        return drawing
    
    def _create_churn_pie_chart(self, stats):
        """Create a pie chart for churn vs stay distribution."""
        drawing = Drawing(400, 200)
        
        pie = Pie()
        pie.x = 150
        pie.y = 25
        pie.width = 150
        pie.height = 150
        
        # Data
        pie.data = [stats['churn_count'], stats['stay_count']]
        pie.labels = [f"Churn ({stats['churn_count']})", f"Stay ({stats['stay_count']})"]
        
        # Colors
        pie.slices[0].fillColor = colors.HexColor('#cf222e')  # Red for churn
        pie.slices[1].fillColor = colors.HexColor('#238636')  # Green for stay
        
        # Styling
        pie.slices.strokeWidth = 2
        pie.slices.strokeColor = colors.white
        pie.sideLabels = True
        pie.simpleLabels = False
        pie.slices.fontName = 'Helvetica-Bold'
        pie.slices.fontSize = 10
        
        drawing.add(pie)
        
        # Add title
        title = String(200, 185, 'Churn vs Stay Prediction', fontSize=12, 
                      fontName='Helvetica-Bold', fillColor=colors.HexColor('#333333'),
                      textAnchor='middle')
        drawing.add(title)
        
        return drawing
    
    def _create_metrics_bar_chart(self):
        """Create a bar chart for model performance metrics."""
        drawing = Drawing(450, 200)
        
        bc = VerticalBarChart()
        bc.x = 60
        bc.y = 30
        bc.height = 130
        bc.width = 350
        
        # Data
        bc.data = [[
            self.model_info['accuracy'],
            self.model_info['precision'],
            self.model_info['recall'],
            self.model_info['f1_score'],
            self.model_info.get('roc_auc', 0)
        ]]
        
        bc.categoryAxis.categoryNames = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
        
        # Styling
        bc.bars[0].fillColor = colors.HexColor('#1f6feb')
        bc.bars.strokeWidth = 0
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 100
        bc.valueAxis.valueStep = 20
        bc.categoryAxis.labels.fontName = 'Helvetica-Bold'
        bc.categoryAxis.labels.fontSize = 9
        bc.valueAxis.labels.fontName = 'Helvetica'
        bc.valueAxis.labels.fontSize = 8
        bc.barWidth = 40
        bc.barSpacing = 20
        
        drawing.add(bc)
        
        # Add title
        title = String(235, 180, 'Model Performance Metrics (%)', fontSize=12, 
                      fontName='Helvetica-Bold', fillColor=colors.HexColor('#333333'),
                      textAnchor='middle')
        drawing.add(title)
        
        return drawing
    
    def _create_risk_distribution(self, stats):
        """Create risk distribution section with optional pie chart."""
        elements = []
        
        elements.append(Paragraph("🎯 Risk Level Distribution", self.styles['SectionHeading']))
        
        # Add pie chart if enabled
        if self.include_charts:
            elements.append(Spacer(1, 10))
            elements.append(self._create_risk_pie_chart(stats))
            elements.append(Spacer(1, 15))
        
        # Risk data table
        risk_data = [
            ['Risk Level', 'Count', 'Percentage', 'Priority'],
            ['🔴 High Risk', str(stats['high_risk']), f"{stats['high_risk']/stats['total']*100:.1f}%", 'Immediate Action'],
            ['🟡 Moderate Risk', str(stats['moderate_risk']), f"{stats['moderate_risk']/stats['total']*100:.1f}%", 'Monitor Closely'],
            ['🟢 Low Risk', str(stats['low_risk']), f"{stats['low_risk']/stats['total']*100:.1f}%", 'Maintain'],
        ]
        
        table = Table(risk_data, colWidths=[1.8*inch, 1*inch, 1.2*inch, 1.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#21262d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            # High risk row
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffebe9')),
            # Moderate risk row
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#fff8c5')),
            # Low risk row
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#dafbe1')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d7de')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_model_performance(self):
        """Create model performance section."""
        elements = []
        
        elements.append(Paragraph("📈 Model Performance Metrics", self.styles['SectionHeading']))
        
        elements.append(Paragraph(
            f"The predictions in this report were generated using <b>{self.model_info['name']}</b> model.",
            self.styles['BodyTextCustom']
        ))
        elements.append(Spacer(1, 10))
        
        # Add bar chart if enabled
        if self.include_charts:
            elements.append(self._create_metrics_bar_chart())
            elements.append(Spacer(1, 15))
        
        # Performance metrics table
        perf_data = [
            ['Metric', 'Value', 'Description'],
            ['ROC-AUC', f"{self.model_info.get('roc_auc', 0):.1f}%", 'Primary selection metric — overall discrimination ability'],
            ['Accuracy', f"{self.model_info['accuracy']:.1f}%", 'Overall correct predictions'],
            ['Precision', f"{self.model_info['precision']:.1f}%", 'Correct churn predictions out of all churn predictions'],
            ['Recall', f"{self.model_info['recall']:.1f}%", 'Churners correctly identified out of all actual churners'],
            ['F1-Score', f"{self.model_info['f1_score']:.1f}%", 'Harmonic mean of precision and recall'],
        ]
        
        table = Table(perf_data, colWidths=[1.2*inch, 1*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#238636')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f6f8fa')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d7de')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_high_risk_customers(self, stats):
        """Create high-risk customers section."""
        elements = []
        
        elements.append(Paragraph("⚠️ High-Risk Customers (Top 15)", self.styles['SectionHeading']))
        
        # Get top high-risk customers sorted by churn probability
        high_risk_df = self.data[self.data['risk_level'] == 'HIGH'].copy()
        if len(high_risk_df) > 0:
            high_risk_df = high_risk_df.sort_values('churn_probability_%', ascending=False).head(15)
            
            # Build table data
            table_data = [['Customer ID', 'Contract', 'Internet', 'Tenure', 'Churn Prob.', 'Risk']]
            
            for _, row in high_risk_df.iterrows():
                customer_id = str(row.get('customerID', row.get('customer_id', 'N/A')))
                contract = str(row.get('Contract', 'N/A'))
                internet = str(row.get('InternetService', 'N/A'))
                tenure = str(int(row.get('tenure', 0))) + ' mo'
                churn_prob = f"{row.get('churn_probability_%', 0):.1f}%"
                risk = row.get('risk_level', 'N/A')
                
                table_data.append([customer_id, contract, internet, tenure, churn_prob, risk])
            
            table = Table(table_data, colWidths=[1.2*inch, 1.2*inch, 1.0*inch, 0.8*inch, 1*inch, 0.8*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#cf222e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffebe9')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d7de')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No high-risk customers found. ✓", self.styles['BodyTextCustom']))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_recommendations(self, stats):
        """Create recommendations section."""
        elements = []
        
        elements.append(Paragraph("💡 Recommendations", self.styles['SectionHeading']))
        
        recommendations = []
        
        if stats['high_risk'] > 0:
            recommendations.append(f"<b>Immediate Outreach:</b> Contact the {stats['high_risk']} high-risk customers immediately with personalized retention offers.")
        
        if stats['churn_rate'] > 30:
            recommendations.append("<b>Review Pricing:</b> High churn rate suggests pricing or value perception issues. Consider promotional discounts.")
        
        if stats['moderate_risk'] > stats['total'] * 0.25:
            recommendations.append("<b>Engagement Campaign:</b> Launch a re-engagement campaign targeting moderate-risk customers to prevent escalation.")
        
        recommendations.append("<b>Contract Upgrades:</b> Incentivize month-to-month customers to switch to one-year or two-year contracts.")
        recommendations.append("<b>Service Bundling:</b> Offer security, backup, and tech support add-ons to customers lacking these services.")
        recommendations.append("<b>Payment Method:</b> Encourage automatic payment methods over electronic checks to reduce churn risk.")
        
        for i, rec in enumerate(recommendations, 1):
            elements.append(Paragraph(f"{i}. {rec}", self.styles['BodyTextCustom']))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_footer(self):
        """Create report footer."""
        elements = []
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("—" * 50, self.styles['CenterText']))
        elements.append(Paragraph(
            "Report generated by ChurnAI Prediction System | Confidential",
            self.styles['CenterText']
        ))
        
        return elements
    
    def _create_roi_section(self, stats):
        """Create ROI Business Impact section for PDF reports."""
        elements = []
        
        CLV_BENEFIT = 450
        CAMPAIGN_COST = 50
        
        high_risk = stats['high_risk']
        moderate_risk = stats['moderate_risk']
        at_risk = high_risk + moderate_risk
        
        high_profit = high_risk * (CLV_BENEFIT - CAMPAIGN_COST)
        mod_profit = moderate_risk * (CLV_BENEFIT - CAMPAIGN_COST)
        total_profit = high_profit + mod_profit
        total_clv = at_risk * CLV_BENEFIT
        total_cost = at_risk * CAMPAIGN_COST
        
        elements.append(Paragraph("💰 ROI Business Impact", self.styles['SectionHeading']))
        
        elements.append(Paragraph(
            f"Following the profit-driven framework of <b>De Caigny et al. (2018)</b>, "
            f"we estimate the business value of retaining at-risk customers. "
            f"Each retained churner saves <b>${CLV_BENEFIT}</b> in Customer Lifetime Value (CLV), "
            f"while each retention campaign costs <b>${CAMPAIGN_COST}</b>.",
            self.styles['BodyTextCustom']
        ))
        elements.append(Spacer(1, 10))
        
        # ROI summary table
        roi_data = [
            ['Tier', 'Customers', 'CLV Saved', 'Campaign Cost', 'Net Profit'],
            ['High Risk', str(high_risk),
             f'${high_risk * CLV_BENEFIT:,}', f'${high_risk * CAMPAIGN_COST:,}',
             f'${high_profit:,}'],
            ['Moderate Risk', str(moderate_risk),
             f'${moderate_risk * CLV_BENEFIT:,}', f'${moderate_risk * CAMPAIGN_COST:,}',
             f'${mod_profit:,}'],
            ['TOTAL', str(at_risk),
             f'${total_clv:,}', f'${total_cost:,}',
             f'${total_profit:,}'],
        ]
        
        table = Table(roi_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#238636')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f6f8fa')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#dafbe1')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d7de')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 10))
        
        # Formula
        elements.append(Paragraph(
            f"<b>Formula:</b> ROI = ({at_risk} x ${CLV_BENEFIT}) - ({at_risk} x ${CAMPAIGN_COST}) "
            f"= ${total_clv:,} - ${total_cost:,} = <b>${total_profit:,}</b>",
            self.styles['BodyTextCustom']
        ))
        elements.append(Spacer(1, 5))
        elements.append(Paragraph(
            "<i>Note: Low-risk customers are excluded — they are unlikely to churn, "
            "so no retention spend is needed.</i>",
            self.styles['BodyTextCustom']
        ))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def generate_summary_report(self, filepath):
        """Generate a summary report PDF."""
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        stats = self._get_summary_stats()
        elements = []
        
        # Build report sections
        elements.extend(self._create_header())
        elements.extend(self._create_executive_summary(stats))
        elements.extend(self._create_risk_distribution(stats))
        elements.extend(self._create_model_performance())
        elements.extend(self._create_high_risk_customers(stats))
        elements.extend(self._create_roi_section(stats))
        elements.extend(self._create_recommendations(stats))
        elements.extend(self._create_footer())
        
        # Build PDF
        doc.build(elements)
        return filepath
    
    def generate_customer_analysis_report(self, filepath):
        """Generate a detailed customer analysis report."""
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=50,
            bottomMargin=50
        )
        
        stats = self._get_summary_stats()
        elements = []
        
        # Header
        elements.extend(self._create_header())
        elements.append(Paragraph("👥 Customer Analysis Report", self.styles['SectionHeading']))
        elements.append(Spacer(1, 10))
        
        # All customers table (grouped by risk)
        for risk_level, risk_name, color in [
            ('HIGH', 'High Risk Customers', '#cf222e'),
            ('MODERATE', 'Moderate Risk Customers', '#bf8700'),
            ('LOW', 'Low Risk Customers', '#238636')
        ]:
            risk_df = self.data[self.data['risk_level'] == risk_level]
            if len(risk_df) > 0:
                elements.append(Paragraph(f"🔸 {risk_name} ({len(risk_df)} customers)", self.styles['SubHeading']))
                
                # Limit to 25 per section
                display_df = risk_df.head(25)
                table_data = [['ID', 'Contract', 'Internet', 'Gender', 'Tenure', 'Churn %']]
                
                for _, row in display_df.iterrows():
                    table_data.append([
                        str(row.get('customerID', row.get('customer_id', 'N/A'))),
                        str(row.get('Contract', 'N/A')),
                        str(row.get('InternetService', 'N/A')),
                        str(row.get('gender', 'N/A')),
                        str(int(row.get('tenure', 0))),
                        f"{row.get('churn_probability_%', 0):.1f}%"
                    ])
                
                table = Table(table_data, colWidths=[0.8*inch, 1.1*inch, 0.9*inch, 0.7*inch, 0.7*inch, 0.8*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(color)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d0d7de')),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ]))
                
                elements.append(table)
                
                if len(risk_df) > 25:
                    elements.append(Paragraph(
                        f"... and {len(risk_df) - 25} more {risk_level.lower()} risk customers",
                        self.styles['CenterText']
                    ))
                
                elements.append(Spacer(1, 15))
        
        elements.extend(self._create_footer())
        doc.build(elements)
        return filepath
    
    def generate_batch_predictions_report(self, filepath):
        """Generate a batch predictions report with all data."""
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=30,
            leftMargin=30,
            topMargin=50,
            bottomMargin=50
        )
        
        stats = self._get_summary_stats()
        elements = []
        
        # Header
        elements.extend(self._create_header())
        elements.append(Paragraph("📋 Batch Prediction Results", self.styles['SectionHeading']))
        elements.append(Paragraph(f"Total Records: {stats['total']}", self.styles['BodyTextCustom']))
        elements.append(Spacer(1, 10))
        
        # Full data table (paginated, 40 per page)
        columns = ['customerID', 'gender', 'Contract', 'InternetService', 'tenure', 'prediction', 'churn_probability_%', 'risk_level']
        display_cols = [col for col in columns if col in self.data.columns]
        
        # Process in chunks
        chunk_size = 40
        total_rows = len(self.data)
        
        for start in range(0, min(total_rows, 120), chunk_size):  # Max 3 pages of data
            end = min(start + chunk_size, total_rows)
            chunk_df = self.data.iloc[start:end]
            
            table_data = [[col.replace('_', ' ').title() for col in display_cols]]
            
            for _, row in chunk_df.iterrows():
                row_data = []
                for col in display_cols:
                    val = row.get(col, 'N/A')
                    if col == 'churn_probability_%':
                        row_data.append(f"{val:.1f}%")
                    elif col in ['tenure', 'SeniorCitizen']:
                        row_data.append(str(int(val)) if val else 'N/A')
                    else:
                        row_data.append(str(val))
                table_data.append(row_data)
            
            col_widths = [0.7*inch, 0.5*inch, 0.7*inch, 1*inch, 0.8*inch, 1*inch, 0.8*inch][:len(display_cols)]
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f6feb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d0d7de')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(f"Rows {start+1} - {end} of {total_rows}", self.styles['CenterText']))
            
            if end < min(total_rows, 120):
                elements.append(PageBreak())
        
        if total_rows > 120:
            elements.append(Paragraph(
                f"Note: This report shows the first 120 records. Export full data as CSV for complete results.",
                self.styles['BodyTextCustom']
            ))
        
        # ROI section
        elements.append(Spacer(1, 15))
        elements.extend(self._create_roi_section(stats))
        
        elements.extend(self._create_footer())
        doc.build(elements)
        return filepath
    
    def generate_model_performance_report(self, filepath):
        """Generate a model performance report."""
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        elements = []
        
        # Header
        elements.extend(self._create_header())
        elements.append(Paragraph("📈 Model Performance Report", self.styles['SectionHeading']))
        elements.append(Spacer(1, 10))
        
        # Model info
        elements.append(Paragraph("Model Information", self.styles['SubHeading']))
        model_data = [
            ['Property', 'Value'],
            ['Algorithm', self.model_info['name']],
            ['Selection Metric', 'ROC-AUC (Area Under ROC Curve)'],
            ['Dataset', 'IBM Telco Customer Churn (7,043 customers)'],
            ['Training Samples', '5,634 (80% stratified split)'],
            ['Test Samples', '1,409 (20% stratified split)'],
            ['Features Used', '46 (after OneHot encoding + feature engineering)'],
            ['Imbalance Handling', 'SMOTE (applied inside CV folds — leakage-proof)'],
            ['Hyperparameter Tuning', 'RandomizedSearchCV (50 iter × 5-fold CV)'],
            ['Cross-Validation', '5-fold Stratified CV, ROC-AUC: 0.8461 ± 0.011'],
            ['Statistical Validation', 'Wilcoxon Signed-Rank Test (10-fold paired CV)'],
            ['ROI (Business Value)', f"${self.model_info.get('roi', 132000):,} = (TP × $450) − (FP × $50)"],
        ]
        
        table = Table(model_data, colWidths=[2.5*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#21262d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f6f8fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d7de')),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Performance metrics
        elements.extend(self._create_model_performance())
        
        # Confusion Matrix
        elements.append(Paragraph("Confusion Matrix (Test Set — 1,409 samples)", self.styles['SubHeading']))
        cm_data = [
            ['', 'Predicted Stay', 'Predicted Churn'],
            ['Actual Stay', '624 (TN)', '411 (FP)'],
            ['Actual Churn', '35 (FN)', '339 (TP)'],
        ]
        
        cm_table = Table(cm_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch])
        cm_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f6feb')),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1f6feb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d7de')),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#dafbe1')),  # True Negative
            ('BACKGROUND', (2, 2), (2, 2), colors.HexColor('#dafbe1')),  # True Positive
            ('BACKGROUND', (2, 1), (2, 1), colors.HexColor('#ffebe9')),  # False Positive
            ('BACKGROUND', (1, 2), (1, 2), colors.HexColor('#ffebe9')),  # False Negative
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(cm_table)
        
        # Confusion matrix interpretation
        elements.append(Spacer(1, 5))
        elements.append(Paragraph(
            "<b>Key Insight:</b> The model catches <b>339 out of 374</b> actual churners (90.64% recall). "
            "It raises 411 false alarms but this is acceptable — it's better to offer retention to a loyal customer "
            "than to miss a churner entirely.",
            self.styles['BodyTextCustom']
        ))
        elements.append(Spacer(1, 20))
        
        # Feature importance
        elements.append(Paragraph("Top Feature Importance (SHAP-based)", self.styles['SubHeading']))
        features = [
            ['Feature', 'Importance', 'Impact'],
            ['Contract', '22%', 'High — Month-to-month contracts strongly predict churn'],
            ['Tenure', '18%', 'High — Newer customers are more likely to churn'],
            ['Internet Service', '15%', 'High — Fiber optic customers churn more frequently'],
            ['Online Security', '10%', 'Medium — Lack of security add-on increases risk'],
            ['Tech Support', '9%', 'Medium — No tech support increases churn likelihood'],
            ['Payment Method', '8%', 'Medium — Electronic check users churn more'],
            ['Monthly Charges', '7%', 'Medium — Higher charges increase churn risk'],
            ['Paperless Billing', '5%', 'Low — Paperless billing slightly increases risk'],
            ['Total Charges', '4%', 'Low — Lower lifetime value indicates newer, riskier customers'],
            ['Dependents', '2%', 'Low — Customers without dependents slightly more likely to churn'],
        ]
        
        feat_table = Table(features, colWidths=[1.5*inch, 1*inch, 3.5*inch])
        feat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#238636')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d0d7de')),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(feat_table)
        
        elements.extend(self._create_footer())
        doc.build(elements)
        return filepath
