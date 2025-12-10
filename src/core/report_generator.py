"""
PDF Report Generator for CS 2500 Extra Credit Project
Generates professional grading reports using ReportLab
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime


def generate_pdf_report(results, output_path):
    """Generate a comprehensive PDF grading report"""

    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    # Container for PDF elements
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20,
        alignment=TA_CENTER
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    # Header
    elements.append(Paragraph("CS 2500 - Extra Credit Project", title_style))
    elements.append(Paragraph("Automated Grading Report", subtitle_style))
    elements.append(Paragraph("Fall 2025", subtitle_style))

    # Add horizontal line
    elements.append(Spacer(1, 0.2 * inch))

    # Student Information
    student_info = [
        ["Student:", results.get("student_name", "Unknown")],
        ["Repository:", results.get("repo_url", "N/A")],
        ["Graded:", results.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))],
        ["Report Generator:", "CS 2500 Autograder v1.0"]
    ]

    info_table = Table(student_info, colWidths=[1.5 * inch, 5 * inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Automated Score Summary (Highlighted Box)
    score = results.get("automated_score", 0)
    max_score = results.get("max_automated_score", 52)
    percentage = (score / max_score * 100) if max_score > 0 else 0

    # Determine status symbol
    if percentage >= 90:
        status_symbol = "✓✓"
        status_color = colors.HexColor('#27ae60')
    elif percentage >= 70:
        status_symbol = "✓"
        status_color = colors.HexColor('#f39c12')
    else:
        status_symbol = "⚠"
        status_color = colors.HexColor('#e74c3c')

    score_data = [[
        f"AUTOMATED SCORE: {score:.1f}/{max_score} points ({percentage:.1f}%) {status_symbol}"
    ]]
    score_table = Table(score_data, colWidths=[6.5 * inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), status_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Check for errors
    if results.get("errors"):
        elements.append(Paragraph("⚠ CRITICAL ERRORS", heading2_style))
        for error in results["errors"]:
            elements.append(Paragraph(f"• {error}", styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(PageBreak())

    # Section 1: File Validation
    elements.append(Paragraph("1. FILE VALIDATION", heading2_style))

    files_found = results.get("files_found", {})

    # Check what's missing
    critical_missing = []
    optional_missing = []
    for filename, exists in files_found.items():
        if not exists:
            if filename in ["graph.py", "dijkstra.py", "astar.py"]:
                critical_missing.append(filename)
            else:
                optional_missing.append(filename)

    # Add note about missing files
    if critical_missing:
        note_text = f"<font color='red'><b>⚠ Critical files missing:</b> {', '.join(critical_missing)}. Cannot grade code without these files.</font>"
        elements.append(Paragraph(note_text, styles['Normal']))
        elements.append(Spacer(1, 0.1 * inch))
    elif optional_missing:
        note_text = f"<font color='orange'><b>ℹ Note:</b> Missing optional files: {', '.join(optional_missing)}. Manual review required.</font>"
        elements.append(Paragraph(note_text, styles['Normal']))
        elements.append(Spacer(1, 0.1 * inch))
    else:
        note_text = "<font color='green'><b>✓</b> All required files present.</font>"
        elements.append(Paragraph(note_text, styles['Normal']))
        elements.append(Spacer(1, 0.1 * inch))

    file_data = [["File", "Status", "Required For"]]
    file_categories = {
        "graph.py": "Automated grading",
        "dijkstra.py": "Automated grading",
        "astar.py": "Automated grading",
        "main.py": "Manual review",
        "DesignDocument.pdf": "Manual grading (20 pts)",
        "README.md": "Manual review",
        "nodes.csv": "Automated grading",
        "edges.csv": "Automated grading"
    }

    for filename, exists in files_found.items():
        status = "✓ Found" if exists else "✗ Missing"
        category = file_categories.get(filename, "Manual review")
        file_data.append([filename, status, category])

    file_table = Table(file_data, colWidths=[2 * inch, 1.5 * inch, 2.5 * inch])
    file_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(file_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Section 2: Graph Operations
    graph_tests = results.get("graph_tests", {})
    if graph_tests:
        elements.append(Paragraph(
            f"2. GRAPH OPERATIONS ({graph_tests.get('total_points', 0):.1f}/{graph_tests.get('max_points', 12)} points)",
            heading2_style
        ))

        test_data = [["Test", "Status", "Details"]]
        for test in graph_tests.get("tests", []):
            status = "✓ PASS" if test["passed"] else "✗ FAIL"
            test_data.append([
                test["name"],
                status,
                test.get("actual", "")
            ])

        test_table = Table(test_data, colWidths=[2 * inch, 1 * inch, 3.5 * inch])
        test_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(test_table)
        elements.append(Spacer(1, 0.3 * inch))

    # Section 3: Dijkstra's Algorithm
    dijkstra_tests = results.get("dijkstra_tests", {})
    if dijkstra_tests:
        elements.append(Paragraph(
            f"3. DIJKSTRA'S ALGORITHM ({dijkstra_tests.get('total_points', 0):.1f}/{dijkstra_tests.get('max_points', 15)} points)",
            heading2_style
        ))

        dijkstra_data = [["Query", "Expected Cost", "Actual Cost", "Nodes Explored", "Status"]]
        for test in dijkstra_tests.get("tests", []):
            dijkstra_data.append([
                f"{test['start']}→{test['end']}",
                str(test.get('expected_cost', 'N/A')),
                f"{test.get('actual_cost', 'N/A'):.1f}" if test.get('actual_cost') else 'N/A',
                str(test.get('nodes_explored', 'N/A')),
                "✓" if test['passed'] else "✗"
            ])

        dijkstra_table = Table(dijkstra_data, colWidths=[1.2 * inch, 1.3 * inch, 1.2 * inch, 1.5 * inch, 0.8 * inch])
        dijkstra_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(dijkstra_table)
        elements.append(Spacer(1, 0.3 * inch))

    # Section 4: A* Algorithm
    astar_tests = results.get("astar_tests", {})
    if astar_tests:
        elements.append(Paragraph(
            f"4. A* ALGORITHM ({astar_tests.get('total_points', 0):.1f}/{astar_tests.get('max_points', 15)} points)",
            heading2_style
        ))

        astar_data = [["Query", "Expected Cost", "Actual Cost", "Nodes Explored", "Status"]]
        for test in astar_tests.get("tests", []):
            astar_data.append([
                f"{test['start']}→{test['end']}",
                str(test.get('expected_cost', 'N/A')),
                f"{test.get('actual_cost', 'N/A'):.1f}" if test.get('actual_cost') else 'N/A',
                str(test.get('nodes_explored', 'N/A')),
                "✓" if test['passed'] else "✗"
            ])

        astar_table = Table(astar_data, colWidths=[1.2 * inch, 1.3 * inch, 1.2 * inch, 1.5 * inch, 0.8 * inch])
        astar_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(astar_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Check for failed tests and show details
        failed_tests = [t for t in astar_tests.get("tests", []) if not t['passed']]
        if failed_tests:
            elements.append(Paragraph("⚠ Issues Found:", styles['Normal']))
            for test in failed_tests:
                issue_text = f"• Query {test['start']}→{test['end']}: "
                if test.get('actual_cost') and test.get('expected_cost'):
                    issue_text += f"returned cost {test['actual_cost']:.1f}, expected {test['expected_cost']:.1f}"
                else:
                    issue_text += "failed to return valid result"
                elements.append(Paragraph(issue_text, styles['Normal']))
            elements.append(Spacer(1, 0.2 * inch))

    # Section 5: Performance Comparison
    perf_tests = results.get("performance_tests", {})
    if perf_tests and perf_tests.get("comparisons"):
        elements.append(PageBreak())
        elements.append(Paragraph(
            f"5. PERFORMANCE COMPARISON ({perf_tests.get('points', 0)}/5 points)",
            heading2_style
        ))

        # Create comparison chart if we have data
        comparisons = perf_tests.get("comparisons", [])

        # Check if we have nodes_explored data
        has_nodes_data = any(c.get("dijkstra_nodes") and c.get("astar_nodes") for c in comparisons)

        if has_nodes_data:
            # Create bar chart
            drawing = Drawing(400, 200)
            chart = VerticalBarChart()
            chart.x = 50
            chart.y = 50
            chart.height = 125
            chart.width = 300

            # Prepare data
            dijkstra_nodes = [c.get("dijkstra_nodes", 0) or 0 for c in comparisons[:5]]
            astar_nodes = [c.get("astar_nodes", 0) or 0 for c in comparisons[:5]]

            chart.data = [dijkstra_nodes, astar_nodes]
            chart.categoryAxis.categoryNames = [f"Q{i + 1}" for i in range(len(comparisons[:5]))]
            chart.bars[0].fillColor = colors.HexColor('#3498db')
            chart.bars[1].fillColor = colors.HexColor('#e74c3c')

            drawing.add(chart)
            elements.append(drawing)
            elements.append(Spacer(1, 0.2 * inch))

            # Legend
            legend_data = [
                ["■ Dijkstra (blue)", "■ A* (red)"]
            ]
            legend_table = Table(legend_data, colWidths=[2 * inch, 2 * inch])
            legend_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#e74c3c')),
            ]))
            elements.append(legend_table)
            elements.append(Spacer(1, 0.2 * inch))

        # Performance table
        perf_data = [["Query", "Dijkstra Nodes", "A* Nodes", "A* Improvement"]]
        for comp in comparisons:
            improvement = comp.get("astar_improvement")
            imp_str = f"{improvement:.1f}%" if improvement is not None else "N/A"

            perf_data.append([
                comp.get("query", "Unknown"),
                str(comp.get("dijkstra_nodes", "N/A")),
                str(comp.get("astar_nodes", "N/A")),
                imp_str
            ])

        perf_table = Table(perf_data, colWidths=[2.5 * inch, 1.3 * inch, 1.2 * inch, 1.5 * inch])
        perf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(perf_table)
        elements.append(Spacer(1, 0.2 * inch))

        # Summary
        if perf_tests.get("tracking_works"):
            elements.append(Paragraph("✓ Both algorithms track nodes_explored", styles['Normal']))

        astar_better = perf_tests.get("astar_better_count", 0)
        total = perf_tests.get("total_queries", 0)
        if total > 0:
            elements.append(Paragraph(
                f"✓ A* explores fewer or equal nodes in {astar_better}/{total} queries",
                styles['Normal']
            ))

    # Section 6: Informational Flags
    flags = results.get("flags", [])
    if flags:
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph("INFORMATIONAL FLAGS", heading2_style))
        elements.append(Paragraph(
            "The following items were detected and may require manual review:",
            styles['Normal']
        ))
        elements.append(Spacer(1, 0.1 * inch))

        for flag in flags:
            flag_type = flag.get("type", "info")
            symbol = "⚠" if flag_type == "warning" else "ℹ"
            message = flag.get("message", "")
            recommendation = flag.get("recommendation", "")

            elements.append(Paragraph(
                f"{symbol} <b>{message}</b>",
                styles['Normal']
            ))
            if recommendation:
                elements.append(Paragraph(
                    f"   → {recommendation}",
                    styles['Normal']
                ))
            elements.append(Spacer(1, 0.05 * inch))

    # Section 7: Manual Grading Requirements
    elements.append(PageBreak())
    elements.append(Paragraph("MANUAL GRADING REQUIRED (98 points)", heading2_style))
    elements.append(Paragraph(
        "The following components require manual review by the instructor:",
        styles['Normal']
    ))
    elements.append(Spacer(1, 0.2 * inch))

    manual_items = [
        ("□", "Code Quality (10 points)", [
            "Priority queue implementation",
            "Code organization and readability",
            "Meaningful comments"
        ]),
        ("□", "Dijkstra's Algorithm (15 points remaining)", [
            "Step-by-step trace (3 pts)",
            "Proof of correctness (8 pts)",
            "Complexity analysis (3 pts)"
        ]),
        ("□", "A* Algorithm (15 points remaining)", [
            "Heuristic admissibility proof (4 pts)",
            "Comparison explanation (3 pts)",
            "Complexity analysis (2 pts)",
            "Algorithm explanation (6 pts)"
        ]),
        ("□", "Design Document (20 points)", [
            "All sections complete and well-written"
        ]),
        ("□", "Algorithm Analysis (15 points)", [
            "Insights and conclusions",
            "Analysis quality"
        ]),
        ("□", "Additional Feature (10 points)", [
            "Properly implemented",
            "Demonstrated in main.py",
            "Documented in report"
        ]),
        ("□", "Testing Quality (5 points)", [
            "Test suite completeness",
            "Edge case coverage"
        ])
    ]

    for checkbox, title, details in manual_items:
        elements.append(Paragraph(f"{checkbox} <b>{title}</b>", styles['Normal']))
        for detail in details:
            elements.append(Paragraph(f"   • {detail}", styles['Normal']))
        elements.append(Spacer(1, 0.1 * inch))

    # Final Summary
    elements.append(Spacer(1, 0.3 * inch))
    summary_data = [[
        "GRADING SUMMARY"
    ], [
        f"Automated Score: {score:.1f}/{max_score} points"
    ], [
        "Manual Review Needed: 0/98 points (not yet graded)"
    ], [
        f"Current Total: {score:.1f}/150 points"
    ]]

    summary_table = Table(summary_data, colWidths=[6.5 * inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#34495e')),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (0, 0), 12),
        ('FONTSIZE', (0, 1), (0, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(summary_table)

    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(
        f"<i>Estimated time to complete manual review: 25 minutes</i>",
        styles['Normal']
    ))

    # Footer
    elements.append(Spacer(1, 0.4 * inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("=" * 80, footer_style))
    elements.append(Paragraph(
        f"End of Automated Report • Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        footer_style
    ))
    elements.append(Paragraph("CS 2500 Autograder v1.0", footer_style))

    # Build PDF
    doc.build(elements)

    return output_path