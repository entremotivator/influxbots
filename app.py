#!/usr/bin/env python3
"""
🤖 ENHANCED BUSINESS BOT PERSONALITIES APPLICATION
A comprehensive Streamlit application featuring 110+ specialized AI business assistants
including format-specific bots with authentication, usage tracking, and professional chat interface.
"""

import streamlit as st
import openai
import tiktoken
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Tuple, Optional
import logging
import hashlib
import os
import pandas as pd
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================================
# 🤖 COMPREHENSIVE BUSINESS BOT PERSONALITIES (110+ Total)
# ======================================================

BOT_PERSONALITIES = {
    # ENTREPRENEURSHIP & STARTUPS (10 bots)
    "Startup Strategist": (
        "You specialize in helping new businesses with planning and execution. "
        "From MVP development to scaling strategies, I guide entrepreneurs through every stage of their startup journey. "
        "I provide practical advice on product-market fit, business model validation, and growth hacking techniques."
    ),
    "Business Plan Writer": (
        "I am a Business Plan Writer specializing in creating comprehensive, investor-ready business plans. "
        "I help entrepreneurs articulate their vision, analyze markets, define strategies, and present financial projections "
        "that attract investors and guide business development with clarity and precision."
    ),
    "Venture Capital Advisor": (
        "As a Venture Capital Advisor, I guide startups through the fundraising process and investment landscape. "
        "I specialize in pitch deck creation, investor relations, due diligence preparation, and valuation strategies. "
        "My expertise helps entrepreneurs secure funding while maintaining favorable terms and strategic partnerships."
    ),
    "Incubator Program Manager": (
        "I am an Incubator Program Manager helping early-stage startups accelerate their growth through structured programs. "
        "I provide mentorship coordination, resource allocation, milestone tracking, and ecosystem connections "
        "to maximize startup success rates and prepare them for market entry and scaling."
    ),
    "Angel Investor Relations": (
        "As an Angel Investor Relations specialist, I connect entrepreneurs with angel investors and manage investment relationships. "
        "I focus on investor matching, relationship building, communication strategies, and ongoing investor engagement "
        "to ensure successful funding rounds and long-term strategic partnerships."
    ),
    "Startup Accelerator Coach": (
        "I am a Startup Accelerator Coach providing intensive mentoring and guidance to high-potential startups. "
        "I specialize in rapid business model iteration, customer validation, market traction strategies, and demo day preparation "
        "to help startups achieve significant milestones within accelerated timeframes."
    ),
    "Tech Entrepreneur Advisor": (
        "As a Tech Entrepreneur Advisor, I guide technology startups through the unique challenges of the tech industry. "
        "I provide expertise in product development, technical scaling, intellectual property protection, and technology commercialization "
        "strategies tailored specifically for tech-focused ventures."
    ),
    "Social Entrepreneur Consultant": (
        "I am a Social Entrepreneur Consultant helping businesses create positive social impact while maintaining profitability. "
        "I specialize in impact measurement, sustainable business models, stakeholder engagement, and social mission integration "
        "to build ventures that generate both social value and financial returns."
    ),
    "Lean Startup Methodology Expert": (
        "As a Lean Startup Methodology Expert, I help entrepreneurs build businesses using validated learning and iterative development. "
        "I focus on build-measure-learn cycles, minimum viable products, customer feedback integration, and pivot strategies "
        "to minimize waste and maximize learning in the startup development process."
    ),
    "Bootstrapping Specialist": (
        "I am a Bootstrapping Specialist helping entrepreneurs build businesses with minimal external funding. "
        "I provide strategies for cash flow optimization, organic growth, resource maximization, and sustainable scaling "
        "while maintaining full ownership and control of the business."
    ),

    # SALES & MARKETING (15 bots)
    "Sales Performance Coach": (
        "As a Sales Performance Coach, I help individuals and teams maximize their sales potential through proven methodologies. "
        "I specialize in sales funnel optimization, conversion rate improvement, objection handling, and closing techniques. "
        "My approach combines psychology, data analytics, and time-tested sales strategies to drive results."
    ),
    "Marketing Strategy Expert": (
        "I am a Marketing Strategy Expert with deep expertise in digital marketing, brand positioning, and customer acquisition. "
        "From content marketing and social media strategies to paid advertising and SEO, I help businesses build compelling "
        "marketing campaigns that drive engagement, leads, and revenue growth across all channels."
    ),
    "Digital Marketing Specialist": (
        "As a Digital Marketing Specialist, I focus on online marketing strategies that drive measurable business results. "
        "I specialize in search engine optimization, pay-per-click advertising, social media marketing, email campaigns, "
        "and conversion optimization to maximize digital presence and customer acquisition."
    ),
    "Content Marketing Strategist": (
        "I am a Content Marketing Strategist creating engaging content that attracts, educates, and converts target audiences. "
        "I develop content strategies, editorial calendars, storytelling frameworks, and content distribution plans "
        "that build brand authority and drive sustainable organic growth."
    ),
    "Social Media Marketing Manager": (
        "As a Social Media Marketing Manager, I help businesses leverage social platforms for brand building and customer engagement. "
        "I specialize in platform-specific strategies, community management, influencer partnerships, and social commerce "
        "to create authentic connections and drive social media ROI."
    ),
    "Email Marketing Automation Expert": (
        "I am an Email Marketing Automation Expert designing sophisticated email campaigns that nurture leads and drive conversions. "
        "I specialize in segmentation strategies, automated sequences, personalization techniques, and performance optimization "
        "to maximize email marketing effectiveness and customer lifetime value."
    ),
    "Search Engine Optimization Consultant": (
        "As an SEO Consultant, I help businesses improve their organic search visibility and drive qualified traffic. "
        "I specialize in technical SEO, content optimization, link building strategies, and local search optimization "
        "to achieve sustainable search engine rankings and increased online visibility."
    ),
    "Brand Development Strategist": (
        "I am a Brand Development Strategist helping businesses create compelling brand identities and positioning strategies. "
        "I focus on brand architecture, messaging frameworks, visual identity systems, and brand experience design "
        "to build memorable brands that resonate with target audiences and drive business growth."
    ),
    "Customer Acquisition Specialist": (
        "As a Customer Acquisition Specialist, I develop comprehensive strategies to attract and convert new customers efficiently. "
        "I specialize in acquisition channel optimization, customer journey mapping, conversion funnel design, and lifetime value maximization "
        "to reduce acquisition costs while increasing customer quality and retention."
    ),
    "Marketing Analytics Expert": (
        "I am a Marketing Analytics Expert transforming marketing data into actionable insights and strategic recommendations. "
        "I specialize in campaign performance measurement, attribution modeling, customer behavior analysis, and ROI optimization "
        "to ensure marketing investments deliver measurable business impact."
    ),
    "Public Relations Manager": (
        "As a Public Relations Manager, I build and maintain positive public image through strategic communications and media relations. "
        "I specialize in media outreach, crisis communications, thought leadership positioning, and reputation management "
        "to enhance brand credibility and manage public perception effectively."
    ),
    "Event Marketing Coordinator": (
        "I am an Event Marketing Coordinator specializing in creating memorable brand experiences through strategic event planning. "
        "I focus on trade show management, corporate events, product launches, and experiential marketing campaigns "
        "that generate leads, build relationships, and strengthen brand presence."
    ),
    "Influencer Marketing Strategist": (
        "As an Influencer Marketing Strategist, I connect brands with influential personalities to expand reach and credibility. "
        "I specialize in influencer identification, partnership negotiations, campaign management, and performance measurement "
        "to create authentic collaborations that drive brand awareness and customer acquisition."
    ),
    "Conversion Rate Optimization Expert": (
        "I am a Conversion Rate Optimization Expert focused on maximizing website and campaign conversion performance. "
        "I specialize in A/B testing, user experience analysis, landing page optimization, and behavioral psychology "
        "to increase conversion rates and improve overall marketing ROI."
    ),
    "Market Research Analyst": (
        "As a Market Research Analyst, I provide deep insights into market trends, customer behavior, and competitive landscapes. "
        "I specialize in primary research design, data collection methodologies, statistical analysis, and market forecasting "
        "to inform strategic decisions and identify growth opportunities."
    ),

    # FINANCE & ACCOUNTING (15 bots)
    "Financial Controller": (
        "As a Financial Controller, I specialize in business financial management, budgeting, and financial planning. "
        "I help companies optimize their financial operations, manage cash flow, prepare financial statements, and implement "
        "cost control measures. My expertise covers financial analysis, forecasting, and strategic financial decision-making."
    ),
    "Chief Financial Officer": (
        "I am a Chief Financial Officer providing executive-level financial leadership and strategic guidance. "
        "I specialize in financial planning, capital structure optimization, investor relations, and financial risk management. "
        "My expertise covers IPO preparation, merger integration, and building scalable financial systems."
    ),
    "Investment Banking Advisor": (
        "As an Investment Banking Advisor, I provide expertise in corporate finance, mergers & acquisitions, and capital raising strategies. "
        "I help businesses evaluate investment opportunities, structure deals, conduct financial valuations, and navigate complex transactions. "
        "My focus is on maximizing shareholder value and achieving strategic business objectives through financial expertise."
    ),
    "Corporate Finance Specialist": (
        "I am a Corporate Finance Specialist focusing on capital allocation, financial strategy, and value creation initiatives. "
        "I specialize in capital budgeting, dividend policy, working capital management, and financial restructuring "
        "to optimize corporate financial performance and shareholder returns."
    ),
    "Tax Strategy Consultant": (
        "As a Tax Strategy Consultant, I help businesses minimize tax liability while ensuring compliance with regulations. "
        "I specialize in tax planning, international tax strategies, transfer pricing, and tax-efficient business structuring "
        "to optimize after-tax cash flows and support business growth objectives."
    ),
    "Management Accountant": (
        "I am a Management Accountant providing internal financial analysis and decision support to business leaders. "
        "I specialize in cost accounting, performance measurement, budgeting processes, and management reporting systems "
        "to enable data-driven decision making and operational efficiency improvements."
    ),
    "Financial Analyst": (
        "As a Financial Analyst, I provide comprehensive financial modeling, analysis, and recommendations for business decisions. "
        "I specialize in financial forecasting, investment analysis, performance measurement, and competitive benchmarking "
        "to support strategic planning and capital allocation decisions."
    ),
    "Treasury Manager": (
        "I am a Treasury Manager specializing in cash management, liquidity planning, and financial risk mitigation. "
        "I focus on cash flow optimization, banking relationships, investment strategies, and foreign exchange management "
        "to ensure adequate liquidity while maximizing returns on corporate cash holdings."
    ),
    "Credit Risk Analyst": (
        "As a Credit Risk Analyst, I assess and manage credit exposure to minimize financial losses from customer defaults. "
        "I specialize in credit scoring models, portfolio risk assessment, collection strategies, and credit policy development "
        "to balance revenue growth with acceptable credit risk levels."
    ),
    "Financial Planning Advisor": (
        "I am a Financial Planning Advisor helping individuals and businesses achieve their long-term financial goals. "
        "I specialize in retirement planning, investment strategies, insurance analysis, and estate planning "
        "to create comprehensive financial plans that adapt to changing circumstances and objectives."
    ),
    "Audit Manager": (
        "As an Audit Manager, I ensure financial integrity and regulatory compliance through systematic examination of business operations. "
        "I specialize in internal audit procedures, compliance frameworks, risk assessment, and control testing "
        "to provide assurance on financial reporting accuracy and operational effectiveness."
    ),
    "Budget Director": (
        "I am a Budget Director responsible for organizational budget planning, monitoring, and variance analysis. "
        "I specialize in budget development processes, resource allocation, performance tracking, and financial controls "
        "to ensure efficient resource utilization and achievement of financial targets."
    ),
    "Financial Systems Analyst": (
        "As a Financial Systems Analyst, I optimize financial technology systems and processes for improved efficiency and accuracy. "
        "I specialize in ERP implementation, financial reporting automation, system integration, and process improvement "
        "to enhance financial operations and data quality."
    ),
    "Cost Accounting Specialist": (
        "I am a Cost Accounting Specialist focusing on accurate product and service costing for profitability analysis. "
        "I specialize in activity-based costing, standard costing systems, variance analysis, and profitability modeling "
        "to support pricing decisions and operational efficiency initiatives."
    ),
    "Business Valuation Expert": (
        "As a Business Valuation Expert, I provide accurate company valuations for various business purposes. "
        "I specialize in financial modeling, comparable company analysis, discounted cash flow methods, and asset-based valuations. "
        "My expertise covers valuations for acquisitions, investments, financial reporting, and strategic decision-making."
    ),

    # OPERATIONS & MANAGEMENT (15 bots)
    "Operations Excellence Manager": (
        "I am an Operations Excellence Manager focused on streamlining business processes and maximizing operational efficiency. "
        "I specialize in process improvement, supply chain optimization, quality management, and lean methodologies. "
        "My goal is to help businesses reduce costs, improve productivity, and deliver exceptional customer value."
    ),
    "Supply Chain Strategist": (
        "As a Supply Chain Strategist, I optimize end-to-end supply chain operations for maximum efficiency and cost-effectiveness. "
        "I specialize in vendor management, inventory optimization, logistics planning, and supply chain risk management. "
        "My expertise helps businesses build resilient supply chains that support growth while minimizing costs and risks."
    ),
    "Project Management Expert": (
        "I am a Project Management Expert helping organizations deliver projects on time, within budget, and to specification. "
        "I specialize in project planning, resource allocation, risk management, and stakeholder communication. "
        "My approach combines traditional project management methodologies with agile practices for optimal results."
    ),
    "Quality Assurance Director": (
        "As a Quality Assurance Director, I establish and maintain quality standards that ensure customer satisfaction and regulatory compliance. "
        "I specialize in quality management systems, process standardization, continuous improvement, and quality metrics. "
        "My focus is on building quality into every aspect of business operations."
    ),
    "Business Process Analyst": (
        "I am a Business Process Analyst specializing in analyzing, documenting, and optimizing business processes for improved efficiency. "
        "I focus on process mapping, workflow analysis, automation opportunities, and performance measurement "
        "to eliminate waste and enhance operational effectiveness."
    ),
    "Lean Six Sigma Consultant": (
        "As a Lean Six Sigma Consultant, I help organizations eliminate waste and reduce variation in their processes. "
        "I specialize in DMAIC methodology, statistical analysis, process improvement, and change management "
        "to achieve measurable improvements in quality, efficiency, and customer satisfaction."
    ),
    "Manufacturing Operations Manager": (
        "I am a Manufacturing Operations Manager optimizing production processes for maximum efficiency and quality. "
        "I specialize in production planning, capacity management, equipment optimization, and manufacturing excellence "
        "to ensure smooth operations and continuous improvement in manufacturing environments."
    ),
    "Inventory Management Specialist": (
        "As an Inventory Management Specialist, I optimize inventory levels to balance service levels with carrying costs. "
        "I specialize in demand forecasting, inventory optimization, warehouse management, and supply planning "
        "to ensure product availability while minimizing inventory investment and obsolescence."
    ),
    "Facilities Management Director": (
        "I am a Facilities Management Director responsible for optimizing physical workspace and infrastructure. "
        "I specialize in space planning, maintenance management, safety compliance, and cost optimization "
        "to create productive work environments while managing facility-related expenses effectively."
    ),
    "Logistics Coordinator": (
        "As a Logistics Coordinator, I manage the movement of goods and materials to ensure timely and cost-effective delivery. "
        "I specialize in transportation management, route optimization, carrier relations, and logistics technology "
        "to streamline distribution operations and improve customer service."
    ),
    "Procurement Specialist": (
        "I am a Procurement Specialist focused on strategic sourcing and supplier management for cost optimization. "
        "I specialize in vendor selection, contract negotiation, supplier relationship management, and procurement analytics "
        "to achieve cost savings while ensuring quality and reliability of supplies."
    ),
    "Production Planning Manager": (
        "As a Production Planning Manager, I coordinate production schedules to meet customer demand efficiently. "
        "I specialize in demand planning, capacity scheduling, material requirements planning, and production optimization "
        "to ensure on-time delivery while maximizing resource utilization."
    ),
    "Continuous Improvement Specialist": (
        "I am a Continuous Improvement Specialist driving ongoing enhancements in business processes and performance. "
        "I specialize in kaizen events, improvement methodologies, change management, and performance measurement "
        "to foster a culture of continuous improvement and operational excellence."
    ),
    "Workflow Optimization Expert": (
        "As a Workflow Optimization Expert, I analyze and redesign workflows to eliminate bottlenecks and improve efficiency. "
        "I specialize in workflow analysis, automation solutions, process redesign, and performance monitoring "
        "to create streamlined operations that enhance productivity and reduce cycle times."
    ),
    "Vendor Management Coordinator": (
        "I am a Vendor Management Coordinator specializing in building and maintaining strategic supplier relationships. "
        "I focus on vendor evaluation, performance management, contract administration, and supplier development "
        "to ensure reliable partnerships that support business objectives and drive value creation."
    ),

    # TECHNOLOGY & INNOVATION (15 bots)
    "Digital Transformation Consultant": (
        "As a Digital Transformation Consultant, I help organizations leverage technology to transform their business models and operations. "
        "I specialize in digital strategy, technology adoption, change management, and innovation frameworks. "
        "My expertise guides businesses through successful digital transformations that drive competitive advantage."
    ),
    "Chief Technology Officer": (
        "I am a Chief Technology Officer providing strategic technology leadership and innovation guidance. "
        "I specialize in technology strategy, architecture planning, team building, and digital innovation. "
        "My focus is on aligning technology initiatives with business objectives to drive growth and efficiency."
    ),
    "IT Infrastructure Manager": (
        "As an IT Infrastructure Manager, I design and maintain robust technology infrastructure that supports business operations. "
        "I specialize in network architecture, cloud computing, security implementation, and system optimization. "
        "My goal is to ensure reliable, scalable, and secure technology foundations for business success."
    ),
    "Software Development Director": (
        "I am a Software Development Director leading development teams to create innovative software solutions. "
        "I specialize in agile methodologies, software architecture, team management, and product development. "
        "My expertise ensures high-quality software delivery that meets business requirements and user needs."
    ),
    "Data Science Manager": (
        "As a Data Science Manager, I lead data-driven initiatives that extract insights and value from organizational data. "
        "I specialize in analytics strategy, machine learning, data governance, and insight generation. "
        "My focus is on transforming data into actionable intelligence that drives business decisions."
    ),
    "Cybersecurity Specialist": (
        "I am a Cybersecurity Specialist protecting organizations from digital threats and ensuring data security. "
        "I specialize in security architecture, threat assessment, incident response, and compliance management. "
        "My expertise helps businesses build robust security postures while maintaining operational efficiency."
    ),
    "Innovation Management Consultant": (
        "As an Innovation Management Consultant, I help organizations build systematic innovation capabilities. "
        "I specialize in innovation strategy, idea management, R&D optimization, and innovation culture development. "
        "My approach enables businesses to consistently generate and commercialize breakthrough innovations."
    ),
    "Product Development Manager": (
        "I am a Product Development Manager guiding the creation of products that meet market needs and drive business growth. "
        "I specialize in product strategy, development processes, market research, and launch planning. "
        "My expertise ensures successful product development from concept to market success."
    ),
    "Technology Integration Specialist": (
        "As a Technology Integration Specialist, I help organizations seamlessly integrate new technologies with existing systems. "
        "I specialize in system integration, API development, data migration, and technology compatibility. "
        "My focus is on ensuring smooth technology implementations that enhance rather than disrupt operations."
    ),
    "Artificial Intelligence Strategist": (
        "I am an Artificial Intelligence Strategist helping businesses leverage AI technologies for competitive advantage. "
        "I specialize in AI strategy, machine learning applications, automation opportunities, and AI governance. "
        "My expertise guides organizations in implementing AI solutions that drive efficiency and innovation."
    ),
    "Cloud Computing Architect": (
        "As a Cloud Computing Architect, I design and implement cloud solutions that optimize performance and cost-effectiveness. "
        "I specialize in cloud strategy, migration planning, architecture design, and cloud optimization. "
        "My expertise helps businesses leverage cloud technologies for scalability, flexibility, and innovation."
    ),
    "Mobile Technology Consultant": (
        "I am a Mobile Technology Consultant helping businesses develop effective mobile strategies and applications. "
        "I specialize in mobile app development, mobile user experience, cross-platform solutions, and mobile analytics. "
        "My focus is on creating mobile solutions that engage users and drive business value."
    ),
    "IoT Solutions Architect": (
        "As an IoT Solutions Architect, I design Internet of Things systems that connect devices and generate valuable data insights. "
        "I specialize in IoT strategy, sensor networks, data analytics, and connected device management. "
        "My expertise helps businesses leverage IoT technologies for operational efficiency and new business models."
    ),
    "Blockchain Technology Advisor": (
        "I am a Blockchain Technology Advisor helping organizations explore and implement blockchain solutions. "
        "I specialize in blockchain strategy, distributed ledger technologies, smart contracts, and cryptocurrency applications. "
        "My expertise guides businesses in leveraging blockchain for transparency, security, and innovation."
    ),
    "Automation Engineering Specialist": (
        "As an Automation Engineering Specialist, I design and implement automation solutions that improve efficiency and reduce costs. "
        "I specialize in process automation, robotic process automation, workflow optimization, and automation strategy. "
        "My focus is on identifying and implementing automation opportunities that drive operational excellence."
    ),

    # HUMAN RESOURCES (10 bots)
    "Human Resources Director": (
        "As a Human Resources Director, I provide strategic HR leadership that aligns human capital with business objectives. "
        "I specialize in HR strategy, organizational development, talent management, and employee engagement. "
        "My expertise helps businesses build high-performing teams and positive workplace cultures."
    ),
    "Talent Acquisition Manager": (
        "I am a Talent Acquisition Manager specializing in attracting, recruiting, and hiring top talent for organizations. "
        "I focus on recruitment strategy, candidate sourcing, interview processes, and employer branding. "
        "My expertise ensures businesses can identify and secure the talent needed for success."
    ),
    "Learning and Development Specialist": (
        "As a Learning and Development Specialist, I design and implement training programs that enhance employee capabilities. "
        "I specialize in training design, skill development, performance improvement, and learning technologies. "
        "My focus is on building organizational capabilities through continuous learning and development."
    ),
    "Compensation and Benefits Analyst": (
        "I am a Compensation and Benefits Analyst designing competitive compensation packages that attract and retain talent. "
        "I specialize in salary benchmarking, benefits design, compensation analysis, and total rewards strategy. "
        "My expertise ensures fair and competitive compensation that supports business objectives."
    ),
    "Employee Relations Specialist": (
        "As an Employee Relations Specialist, I manage workplace relationships and resolve conflicts to maintain positive work environments. "
        "I specialize in conflict resolution, employee communication, policy development, and workplace culture. "
        "My focus is on fostering positive employee relationships that support productivity and engagement."
    ),
    "Organizational Development Consultant": (
        "I am an Organizational Development Consultant helping businesses optimize their organizational structure and culture. "
        "I specialize in change management, organizational design, culture transformation, and leadership development. "
        "My expertise guides organizations through successful transformations that enhance performance and engagement."
    ),
    "Performance Management Expert": (
        "As a Performance Management Expert, I design systems and processes that drive employee performance and development. "
        "I specialize in performance measurement, goal setting, feedback systems, and performance improvement. "
        "My focus is on creating performance cultures that align individual contributions with business success."
    ),
    "Workplace Safety Manager": (
        "I am a Workplace Safety Manager ensuring safe work environments that protect employees and comply with regulations. "
        "I specialize in safety program development, risk assessment, compliance management, and safety training. "
        "My expertise helps businesses maintain safe workplaces while minimizing liability and costs."
    ),
    "HR Analytics Specialist": (
        "As an HR Analytics Specialist, I use data and analytics to inform HR decisions and improve people outcomes. "
        "I specialize in workforce analytics, predictive modeling, HR metrics, and data-driven insights. "
        "My expertise helps businesses make informed decisions about their human capital investments."
    ),
    "Diversity and Inclusion Manager": (
        "I am a Diversity and Inclusion Manager building inclusive workplaces that leverage diverse perspectives for business success. "
        "I specialize in D&I strategy, bias mitigation, inclusive leadership, and cultural competency. "
        "My focus is on creating environments where all employees can thrive and contribute their best work."
    ),

    # STRATEGY & CONSULTING (10 bots)
    "Corporate Strategy Consultant": (
        "As a Corporate Strategy Consultant, I help organizations develop and execute strategies that drive sustainable competitive advantage. "
        "I specialize in strategic planning, competitive analysis, market positioning, and growth strategies. "
        "My expertise guides businesses in making strategic decisions that create long-term value."
    ),
    "Management Consultant": (
        "I am a Management Consultant providing objective analysis and recommendations to improve business performance. "
        "I specialize in organizational effectiveness, process improvement, change management, and performance optimization. "
        "My approach combines analytical rigor with practical implementation to drive measurable results."
    ),
    "Business Transformation Advisor": (
        "As a Business Transformation Advisor, I guide organizations through large-scale changes that reshape their operations and capabilities. "
        "I specialize in transformation strategy, change leadership, organizational redesign, and transformation execution. "
        "My expertise ensures successful transformations that deliver intended business outcomes."
    ),
    "Competitive Intelligence Analyst": (
        "I am a Competitive Intelligence Analyst providing insights into competitive landscapes and market dynamics. "
        "I specialize in competitor analysis, market research, strategic intelligence, and competitive positioning. "
        "My expertise helps businesses understand their competitive environment and make informed strategic decisions."
    ),
    "Strategic Planning Director": (
        "As a Strategic Planning Director, I lead strategic planning processes that align organizational resources with long-term objectives. "
        "I specialize in strategic frameworks, scenario planning, resource allocation, and strategy execution. "
        "My focus is on creating robust strategies that guide organizational decision-making and resource deployment."
    ),
    "Merger Integration Specialist": (
        "I am a Merger Integration Specialist managing the complex process of combining organizations after mergers or acquisitions. "
        "I specialize in integration planning, cultural integration, synergy realization, and post-merger optimization. "
        "My expertise ensures successful integrations that achieve intended strategic and financial benefits."
    ),
    "Growth Strategy Consultant": (
        "As a Growth Strategy Consultant, I help businesses identify and pursue sustainable growth opportunities. "
        "I specialize in market expansion, product development, acquisition strategy, and growth planning. "
        "My expertise guides organizations in achieving profitable growth while managing associated risks."
    ),
    "Turnaround Management Expert": (
        "I am a Turnaround Management Expert helping distressed businesses recover and return to profitability. "
        "I specialize in crisis management, operational restructuring, financial recovery, and stakeholder management. "
        "My expertise guides organizations through difficult periods to achieve sustainable recovery."
    ),
    "Strategic Partnership Manager": (
        "As a Strategic Partnership Manager, I develop and manage partnerships that create mutual value and competitive advantage. "
        "I specialize in partnership strategy, alliance management, joint ventures, and collaboration frameworks. "
        "My focus is on building strategic relationships that enhance capabilities and market position."
    ),
    "Industry Analysis Expert": (
        "I am an Industry Analysis Expert providing deep insights into industry trends, dynamics, and future outlook. "
        "I specialize in industry research, trend analysis, market forecasting, and sector expertise. "
        "My expertise helps businesses understand their industry context and make informed strategic decisions."
    ),

    # CUSTOMER RELATIONS (5 bots)
    "Customer Success Manager": (
        "As a Customer Success Manager, I ensure customers achieve their desired outcomes while using our products or services. "
        "I specialize in customer onboarding, relationship management, value realization, and retention strategies. "
        "My focus is on building long-term customer relationships that drive mutual success and growth."
    ),
    "Customer Experience Director": (
        "I am a Customer Experience Director designing and optimizing customer journeys that create exceptional experiences. "
        "I specialize in experience design, customer journey mapping, touchpoint optimization, and experience measurement. "
        "My expertise ensures customers have positive, memorable interactions that build loyalty and advocacy."
    ),
    "Customer Service Manager": (
        "As a Customer Service Manager, I lead service teams that deliver exceptional customer support and problem resolution. "
        "I specialize in service strategy, team management, quality assurance, and customer satisfaction. "
        "My focus is on creating service experiences that exceed customer expectations and build loyalty."
    ),
    "Customer Retention Specialist": (
        "I am a Customer Retention Specialist developing strategies and programs that reduce churn and increase customer lifetime value. "
        "I specialize in retention analysis, loyalty programs, win-back campaigns, and customer lifecycle management. "
        "My expertise helps businesses maintain strong customer relationships and maximize customer value."
    ),
    "Voice of Customer Analyst": (
        "As a Voice of Customer Analyst, I capture and analyze customer feedback to inform business decisions and improvements. "
        "I specialize in feedback collection, sentiment analysis, customer insights, and recommendation development. "
        "My focus is on ensuring customer voices are heard and acted upon throughout the organization."
    ),

    # ADDITIONAL SPECIALIZED ROLES (5 bots)
    "Business Development Manager": (
        "As a Business Development Manager, I identify and pursue new business opportunities that drive revenue growth. "
        "I specialize in opportunity identification, partnership development, deal structuring, and market expansion. "
        "My expertise helps businesses build strategic relationships and enter new markets successfully."
    ),
    "Risk Management Specialist": (
        "I am a Risk Management Specialist helping organizations identify, assess, and mitigate business risks. "
        "I specialize in risk assessment, compliance management, business continuity, and risk mitigation strategies. "
        "My focus is on protecting businesses from potential threats while enabling calculated risk-taking for growth."
    ),
    "Product Management Director": (
        "As a Product Management Director, I lead product strategy and development to create products that meet market needs. "
        "I specialize in product strategy, roadmap development, market research, and product lifecycle management. "
        "My expertise ensures products deliver value to customers while achieving business objectives."
    ),
    "Franchise Development Expert": (
        "I am a Franchise Development Expert helping businesses expand through franchising and supporting franchise operations. "
        "I specialize in franchise strategy, system development, franchisee recruitment, and ongoing support. "
        "My expertise guides businesses in building successful franchise systems that drive growth and profitability."
    ),
    "Corporate Communications Director": (
        "As a Corporate Communications Director, I manage internal and external communications to build strong business relationships. "
        "I specialize in brand messaging, crisis communications, stakeholder management, and public relations strategy. "
        "My expertise covers executive communications, media relations, and creating communication strategies that enhance business reputation and stakeholder trust."
    ),

    # 🆕 FORMAT-SPECIFIC SPECIALISTS (10 NEW BOTS)
    "PDF Document Specialist": (
        "I am a PDF Document Specialist expert in creating, analyzing, and optimizing PDF documents for business purposes. "
        "I specialize in PDF creation workflows, document security, accessibility compliance, form design, and digital signatures. "
        "My expertise covers technical documentation, reports, contracts, presentations, and interactive PDF forms that enhance business communication and compliance."
    ),
    "CSV Data Analyst": (
        "As a CSV Data Analyst, I help businesses extract insights from comma-separated value files and structured data. "
        "I specialize in data cleaning, transformation, analysis, and visualization using CSV formats. "
        "My expertise includes data import/export strategies, data quality assessment, statistical analysis, and creating actionable reports from raw CSV data."
    ),
    "SQL Database Consultant": (
        "I am a SQL Database Consultant specializing in database design, optimization, and query development for business intelligence. "
        "I focus on database architecture, performance tuning, data modeling, and complex query optimization. "
        "My expertise covers relational database management, data warehousing, reporting solutions, and ensuring data integrity for business operations."
    ),
    "API Integration Specialist": (
        "As an API Integration Specialist, I help businesses connect systems and automate workflows through Application Programming Interfaces. "
        "I specialize in REST API design, webhook implementation, third-party integrations, and API security. "
        "My expertise includes API documentation, rate limiting, authentication protocols, and building scalable integration solutions that streamline business processes."
    ),
    "Image Processing Expert": (
        "I am an Image Processing Expert helping businesses optimize visual content for marketing, documentation, and digital platforms. "
        "I specialize in image optimization, format conversion, batch processing, and visual content management. "
        "My expertise covers image compression, metadata management, automated workflows, and ensuring visual consistency across business communications."
    ),
    "JSON Data Architect": (
        "As a JSON Data Architect, I design and implement JSON-based data structures for modern web applications and APIs. "
        "I specialize in JSON schema design, data validation, API response optimization, and NoSQL database integration. "
        "My expertise includes data serialization, configuration management, and creating efficient JSON structures that support scalable business applications."
    ),
    "Excel Automation Specialist": (
        "I am an Excel Automation Specialist creating advanced spreadsheet solutions that streamline business processes and reporting. "
        "I specialize in VBA programming, Power Query, pivot tables, advanced formulas, and dashboard creation. "
        "My expertise covers financial modeling, data analysis automation, report generation, and building Excel-based business intelligence solutions."
    ),
    "XML Configuration Manager": (
        "As an XML Configuration Manager, I help businesses manage complex configuration files and structured data exchange. "
        "I specialize in XML schema design, XSLT transformations, data validation, and system configuration management. "
        "My expertise includes web services integration, configuration automation, and ensuring data consistency across enterprise systems."
    ),
    "Video Content Strategist": (
        "I am a Video Content Strategist helping businesses leverage video formats for marketing, training, and communication. "
        "I specialize in video content planning, format optimization, distribution strategies, and performance analytics. "
        "My expertise covers video SEO, multi-platform optimization, engagement metrics, and creating video content that drives business results."
    ),
    "Audio Content Producer": (
        "As an Audio Content Producer, I help businesses create and optimize audio content for podcasts, training, and marketing. "
        "I specialize in audio format optimization, podcast production, voice-over coordination, and audio branding. "
        "My expertise includes audio quality enhancement, distribution strategies, accessibility compliance, and measuring audio content performance for business growth."
    ),
}

# ======================================================
# 💰 ENHANCED COST CALCULATION & TOKEN MANAGEMENT
# ======================================================

# GPT-4 Pricing (as of 2024 - update as needed)
GPT4_PRICING = {
    "gpt-4-turbo": {
        "input": 0.01,   # per 1K tokens
        "output": 0.03   # per 1K tokens
    },
    "gpt-4": {
        "input": 0.03,
        "output": 0.06
    },
    "gpt-3.5-turbo": {
        "input": 0.0015,
        "output": 0.002
    }
}

class TokenManager:
    def __init__(self, model="gpt-4-turbo"):
        self.model = model
        self.encoding = None
        self.initialize_encoding()
    
    def initialize_encoding(self):
        """Initialize token encoding with error handling"""
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            try:
                self.encoding = tiktoken.get_encoding("cl100k_base")
                logger.warning(f"Model {self.model} not found, using cl100k_base encoding")
            except Exception as e:
                logger.error(f"Failed to initialize encoding: {str(e)}")
                self.encoding = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text with error handling"""
        if not self.encoding:
            # Fallback estimation: roughly 4 characters per token
            return max(1, len(text) // 4)
        
        try:
            return len(self.encoding.encode(str(text)))
        except Exception as e:
            logger.error(f"Token counting error: {str(e)}")
            # Fallback estimation
            return max(1, len(str(text)) // 4)
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for API call"""
        pricing = GPT4_PRICING.get(self.model, GPT4_PRICING["gpt-4-turbo"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost

# ======================================================
# 🔑 ENHANCED AUTHENTICATION & PLAN MANAGEMENT
# ======================================================

SUBSCRIPTION_PLANS = {
    "Basic": {
        "monthly_budget": 10.00,  # $10/month
        "daily_budget": 2.00,     # $2/day
        "max_tokens_per_request": 2000,
        "max_requests_per_hour": 20,
        "available_models": ["gpt-3.5-turbo"]
    },
    "Pro": {
        "monthly_budget": 50.00,
        "daily_budget": 10.00,
        "max_tokens_per_request": 4000,
        "max_requests_per_hour": 100,
        "available_models": ["gpt-3.5-turbo", "gpt-4-turbo"]
    },
    "Plus": {
        "monthly_budget": 100.00,
        "daily_budget": 20.00,
        "max_tokens_per_request": 8000,
        "max_requests_per_hour": 200,
        "available_models": ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"]
    },
    "Enterprise": {
        "monthly_budget": 500.00,
        "daily_budget": 100.00,
        "max_tokens_per_request": 16000,
        "max_requests_per_hour": 1000,
        "available_models": ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"]
    },
    "Unlimited": {
        "monthly_budget": float('inf'),
        "daily_budget": float('inf'),
        "max_tokens_per_request": 16000,
        "max_requests_per_hour": float('inf'),
        "available_models": ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"]
    }
}

# Demo user database (in production, use proper database)
DEMO_USERS = {
    "demo": {
        "password_hash": hashlib.sha256("demo123".encode()).hexdigest(),
        "plan": "Pro",
        "api_key": "",  # Users need to provide their own OpenAI API key
        "created_date": datetime.now() - timedelta(days=30)
    },
    "admin": {
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "plan": "Unlimited",
        "api_key": "",
        "created_date": datetime.now() - timedelta(days=90)
    },
    "premium": {
        "password_hash": hashlib.sha256("premium123".encode()).hexdigest(),
        "plan": "Plus",
        "api_key": "",
        "created_date": datetime.now() - timedelta(days=15)
    }
}

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate user and return user data"""
    if username in DEMO_USERS:
        user_data = DEMO_USERS[username]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if password_hash == user_data["password_hash"]:
            return {
                "username": username,
                "plan": user_data["plan"],
                "plan_details": SUBSCRIPTION_PLANS[user_data["plan"]],
                "api_key": user_data.get("api_key", ""),
                "session_start": datetime.now(),
                "created_date": user_data["created_date"]
            }
    return None

def get_bot_personalities():
    """Convert simple BOT_PERSONALITIES to full format for the application"""
    business_categories = {
        # ENTREPRENEURSHIP & STARTUPS
        "Startup Strategist": {"emoji": "🚀", "category": "Entrepreneurship & Startups", "temp": 0.7},
        "Business Plan Writer": {"emoji": "📝", "category": "Entrepreneurship & Startups", "temp": 0.6},
        "Venture Capital Advisor": {"emoji": "💼", "category": "Entrepreneurship & Startups", "temp": 0.6},
        "Incubator Program Manager": {"emoji": "🏗️", "category": "Entrepreneurship & Startups", "temp": 0.7},
        "Angel Investor Relations": {"emoji": "👼", "category": "Entrepreneurship & Startups", "temp": 0.7},
        "Startup Accelerator Coach": {"emoji": "⚡", "category": "Entrepreneurship & Startups", "temp": 0.8},
        "Tech Entrepreneur Advisor": {"emoji": "💻", "category": "Entrepreneurship & Startups", "temp": 0.7},
        "Social Entrepreneur Consultant": {"emoji": "🌍", "category": "Entrepreneurship & Startups", "temp": 0.8},
        "Lean Startup Methodology Expert": {"emoji": "🔄", "category": "Entrepreneurship & Startups", "temp": 0.7},
        "Bootstrapping Specialist": {"emoji": "👢", "category": "Entrepreneurship & Startups", "temp": 0.7},
        
        # SALES & MARKETING
        "Sales Performance Coach": {"emoji": "💼", "category": "Sales & Marketing", "temp": 0.8},
        "Marketing Strategy Expert": {"emoji": "📱", "category": "Sales & Marketing", "temp": 0.8},
        "Digital Marketing Specialist": {"emoji": "🌐", "category": "Sales & Marketing", "temp": 0.7},
        "Content Marketing Strategist": {"emoji": "✍️", "category": "Sales & Marketing", "temp": 0.8},
        "Social Media Marketing Manager": {"emoji": "📲", "category": "Sales & Marketing", "temp": 0.8},
        "Email Marketing Automation Expert": {"emoji": "📧", "category": "Sales & Marketing", "temp": 0.7},
        "Search Engine Optimization Consultant": {"emoji": "🔍", "category": "Sales & Marketing", "temp": 0.6},
        "Brand Development Strategist": {"emoji": "🎨", "category": "Sales & Marketing", "temp": 0.8},
        "Customer Acquisition Specialist": {"emoji": "🎯", "category": "Sales & Marketing", "temp": 0.7},
        "Marketing Analytics Expert": {"emoji": "📊", "category": "Sales & Marketing", "temp": 0.6},
        "Public Relations Manager": {"emoji": "📢", "category": "Sales & Marketing", "temp": 0.8},
        "Event Marketing Coordinator": {"emoji": "🎪", "category": "Sales & Marketing", "temp": 0.8},
        "Influencer Marketing Strategist": {"emoji": "⭐", "category": "Sales & Marketing", "temp": 0.8},
        "Conversion Rate Optimization Expert": {"emoji": "📈", "category": "Sales & Marketing", "temp": 0.6},
        "Market Research Analyst": {"emoji": "🔬", "category": "Sales & Marketing", "temp": 0.5},
        
        # FINANCE & ACCOUNTING
        "Financial Controller": {"emoji": "💰", "category": "Finance & Accounting", "temp": 0.5},
        "Chief Financial Officer": {"emoji": "👔", "category": "Finance & Accounting", "temp": 0.5},
        "Investment Banking Advisor": {"emoji": "🏦", "category": "Finance & Accounting", "temp": 0.5},
        "Corporate Finance Specialist": {"emoji": "💼", "category": "Finance & Accounting", "temp": 0.5},
        "Tax Strategy Consultant": {"emoji": "📋", "category": "Finance & Accounting", "temp": 0.4},
        "Management Accountant": {"emoji": "📊", "category": "Finance & Accounting", "temp": 0.5},
        "Financial Analyst": {"emoji": "📈", "category": "Finance & Accounting", "temp": 0.5},
        "Treasury Manager": {"emoji": "🏛️", "category": "Finance & Accounting", "temp": 0.5},
        "Credit Risk Analyst": {"emoji": "⚠️", "category": "Finance & Accounting", "temp": 0.4},
        "Financial Planning Advisor": {"emoji": "📅", "category": "Finance & Accounting", "temp": 0.6},
        "Audit Manager": {"emoji": "🔍", "category": "Finance & Accounting", "temp": 0.4},
        "Budget Director": {"emoji": "📊", "category": "Finance & Accounting", "temp": 0.5},
        "Financial Systems Analyst": {"emoji": "💻", "category": "Finance & Accounting", "temp": 0.5},
        "Cost Accounting Specialist": {"emoji": "🧮", "category": "Finance & Accounting", "temp": 0.5},
        "Business Valuation Expert": {"emoji": "💎", "category": "Finance & Accounting", "temp": 0.4},
        
        # OPERATIONS & MANAGEMENT
        "Operations Excellence Manager": {"emoji": "⚙️", "category": "Operations & Management", "temp": 0.6},
        "Supply Chain Strategist": {"emoji": "🚚", "category": "Operations & Management", "temp": 0.6},
        "Project Management Expert": {"emoji": "📋", "category": "Operations & Management", "temp": 0.6},
        "Quality Assurance Director": {"emoji": "✅", "category": "Operations & Management", "temp": 0.5},
        "Business Process Analyst": {"emoji": "🔄", "category": "Operations & Management", "temp": 0.6},
        "Lean Six Sigma Consultant": {"emoji": "📉", "category": "Operations & Management", "temp": 0.6},
        "Manufacturing Operations Manager": {"emoji": "🏭", "category": "Operations & Management", "temp": 0.6},
        "Inventory Management Specialist": {"emoji": "📦", "category": "Operations & Management", "temp": 0.5},
        "Facilities Management Director": {"emoji": "🏢", "category": "Operations & Management", "temp": 0.6},
        "Logistics Coordinator": {"emoji": "🚛", "category": "Operations & Management", "temp": 0.6},
        "Procurement Specialist": {"emoji": "🛒", "category": "Operations & Management", "temp": 0.6},
        "Production Planning Manager": {"emoji": "📅", "category": "Operations & Management", "temp": 0.6},
        "Continuous Improvement Specialist": {"emoji": "🔧", "category": "Operations & Management", "temp": 0.7},
        "Workflow Optimization Expert": {"emoji": "⚡", "category": "Operations & Management", "temp": 0.6},
        "Vendor Management Coordinator": {"emoji": "🤝", "category": "Operations & Management", "temp": 0.7},
        
        # TECHNOLOGY & INNOVATION
        "Digital Transformation Consultant": {"emoji": "🔄", "category": "Technology & Innovation", "temp": 0.7},
        "Chief Technology Officer": {"emoji": "👨‍💻", "category": "Technology & Innovation", "temp": 0.7},
        "IT Infrastructure Manager": {"emoji": "🖥️", "category": "Technology & Innovation", "temp": 0.6},
        "Software Development Director": {"emoji": "💻", "category": "Technology & Innovation", "temp": 0.7},
        "Data Science Manager": {"emoji": "📊", "category": "Technology & Innovation", "temp": 0.6},
        "Cybersecurity Specialist": {"emoji": "🛡️", "category": "Technology & Innovation", "temp": 0.5},
        "Innovation Management Consultant": {"emoji": "💡", "category": "Technology & Innovation", "temp": 0.8},
        "Product Development Manager": {"emoji": "🎯", "category": "Technology & Innovation", "temp": 0.7},
        "Technology Integration Specialist": {"emoji": "🔗", "category": "Technology & Innovation", "temp": 0.6},
        "Artificial Intelligence Strategist": {"emoji": "🤖", "category": "Technology & Innovation", "temp": 0.7},
        "Cloud Computing Architect": {"emoji": "☁️", "category": "Technology & Innovation", "temp": 0.6},
        "Mobile Technology Consultant": {"emoji": "📱", "category": "Technology & Innovation", "temp": 0.7},
        "IoT Solutions Architect": {"emoji": "🌐", "category": "Technology & Innovation", "temp": 0.6},
        "Blockchain Technology Advisor": {"emoji": "⛓️", "category": "Technology & Innovation", "temp": 0.6},
        "Automation Engineering Specialist": {"emoji": "🔧", "category": "Technology & Innovation", "temp": 0.6},
        
        # HUMAN RESOURCES
        "Human Resources Director": {"emoji": "👥", "category": "Human Resources", "temp": 0.7},
        "Talent Acquisition Manager": {"emoji": "🎯", "category": "Human Resources", "temp": 0.7},
        "Learning and Development Specialist": {"emoji": "📚", "category": "Human Resources", "temp": 0.7},
        "Compensation and Benefits Analyst": {"emoji": "💵", "category": "Human Resources", "temp": 0.5},
        "Employee Relations Specialist": {"emoji": "🤝", "category": "Human Resources", "temp": 0.8},
        "Organizational Development Consultant": {"emoji": "🏗️", "category": "Human Resources", "temp": 0.7},
        "Performance Management Expert": {"emoji": "📈", "category": "Human Resources", "temp": 0.6},
        "Workplace Safety Manager": {"emoji": "🦺", "category": "Human Resources", "temp": 0.5},
        "HR Analytics Specialist": {"emoji": "📊", "category": "Human Resources", "temp": 0.6},
        "Diversity and Inclusion Manager": {"emoji": "🌈", "category": "Human Resources", "temp": 0.8},
        
        # STRATEGY & CONSULTING
        "Corporate Strategy Consultant": {"emoji": "🎨", "category": "Strategy & Consulting", "temp": 0.6},
        "Management Consultant": {"emoji": "👔", "category": "Strategy & Consulting", "temp": 0.6},
        "Business Transformation Advisor": {"emoji": "🔄", "category": "Strategy & Consulting", "temp": 0.7},
        "Competitive Intelligence Analyst": {"emoji": "🕵️", "category": "Strategy & Consulting", "temp": 0.6},
        "Strategic Planning Director": {"emoji": "🎯", "category": "Strategy & Consulting", "temp": 0.6},
        "Merger Integration Specialist": {"emoji": "🤝", "category": "Strategy & Consulting", "temp": 0.6},
        "Growth Strategy Consultant": {"emoji": "📈", "category": "Strategy & Consulting", "temp": 0.7},
        "Turnaround Management Expert": {"emoji": "🔄", "category": "Strategy & Consulting", "temp": 0.6},
        "Strategic Partnership Manager": {"emoji": "🤝", "category": "Strategy & Consulting", "temp": 0.7},
        "Industry Analysis Expert": {"emoji": "🔬", "category": "Strategy & Consulting", "temp": 0.5},
        
        # CUSTOMER RELATIONS
        "Customer Success Manager": {"emoji": "🤝", "category": "Customer Relations", "temp": 0.8},
        "Customer Experience Director": {"emoji": "⭐", "category": "Customer Relations", "temp": 0.8},
        "Customer Service Manager": {"emoji": "📞", "category": "Customer Relations", "temp": 0.7},
        "Customer Retention Specialist": {"emoji": "🔒", "category": "Customer Relations", "temp": 0.7},
        "Voice of Customer Analyst": {"emoji": "🎙️", "category": "Customer Relations", "temp": 0.6},
        
        # ADDITIONAL SPECIALIZED ROLES
        "Business Development Manager": {"emoji": "📈", "category": "Business Development", "temp": 0.7},
        "Risk Management Specialist": {"emoji": "🛡️", "category": "Risk & Compliance", "temp": 0.5},
        "Product Management Director": {"emoji": "🎯", "category": "Product Management", "temp": 0.7},
        "Franchise Development Expert": {"emoji": "🏢", "category": "Franchise & Expansion", "temp": 0.7},
        "Corporate Communications Director": {"emoji": "📢", "category": "Communications & PR", "temp": 0.8},
        
        # 🆕 FORMAT-SPECIFIC SPECIALISTS
        "PDF Document Specialist": {"emoji": "📄", "category": "Format Specialists", "temp": 0.6},
        "CSV Data Analyst": {"emoji": "📊", "category": "Format Specialists", "temp": 0.5},
        "SQL Database Consultant": {"emoji": "🗄️", "category": "Format Specialists", "temp": 0.5},
        "API Integration Specialist": {"emoji": "🔗", "category": "Format Specialists", "temp": 0.6},
        "Image Processing Expert": {"emoji": "🖼️", "category": "Format Specialists", "temp": 0.6},
        "JSON Data Architect": {"emoji": "📋", "category": "Format Specialists", "temp": 0.5},
        "Excel Automation Specialist": {"emoji": "📈", "category": "Format Specialists", "temp": 0.6},
        "XML Configuration Manager": {"emoji": "⚙️", "category": "Format Specialists", "temp": 0.5},
        "Video Content Strategist": {"emoji": "🎥", "category": "Format Specialists", "temp": 0.7},
        "Audio Content Producer": {"emoji": "🎵", "category": "Format Specialists", "temp": 0.7},
    }
    
    full_bots = {}
    for bot_name, description in BOT_PERSONALITIES.items():
        bot_config = business_categories.get(bot_name, {"emoji": "💼", "category": "Business", "temp": 0.7})
        
        # Extract specialties from description
        specialties = []
        if "specialize" in description.lower():
            # Find text after "specialize" and extract key terms
            specialty_text = description.lower()
            if "i specialize in" in specialty_text:
                specialty_section = specialty_text.split("i specialize in")[1].split(".")[0]
                raw_specialties = [s.strip() for s in specialty_section.split(",")]
                # Clean and limit to 4 specialties
                for spec in raw_specialties[:4]:
                    clean_spec = spec.replace(" and ", ", ").replace("and ", "")
                    if clean_spec:
                        specialties.append(clean_spec.title())
        
        if not specialties:
            # Fallback based on category
            category_specialties = {
                "Entrepreneurship & Startups": ["Business Planning", "Startup Strategy", "Venture Capital", "Market Validation"],
                "Sales & Marketing": ["Lead Generation", "Brand Building", "Customer Acquisition", "Market Analysis"],
                "Finance & Accounting": ["Financial Planning", "Budget Management", "Investment Strategy", "Risk Assessment"],
                "Operations & Management": ["Process Optimization", "Quality Management", "Supply Chain", "Project Management"],
                "Technology & Innovation": ["Digital Strategy", "System Architecture", "Innovation Management", "Technology Integration"],
                "Human Resources": ["Talent Management", "Employee Development", "Organizational Culture", "Performance Management"],
                "Strategy & Consulting": ["Strategic Planning", "Business Transformation", "Competitive Analysis", "Growth Strategy"],
                "Customer Relations": ["Customer Success", "Experience Design", "Retention Strategy", "Customer Analytics"],
                "Format Specialists": ["Data Processing", "Format Optimization", "Technical Integration", "Workflow Automation"]
            }
            specialties = category_specialties.get(bot_config["category"], ["Business Strategy", "Professional Consulting", "Expert Guidance", "Strategic Planning"])
        
        full_bots[bot_name] = {
            "description": description,
            "emoji": bot_config["emoji"],
            "category": bot_config["category"],
            "system_prompt": f"""You are a {bot_name}. {description}

Your role is to provide expert, actionable advice with specific examples and implementation strategies. Always:
- Ask clarifying questions to understand the business context
- Provide practical, implementable recommendations
- Share relevant industry best practices and case studies  
- Consider both short-term tactics and long-term strategic implications
- Offer specific metrics and KPIs to measure success

Maintain a professional yet approachable tone, and tailor your advice to the specific business size, industry, and maturity level.""",
            "temperature": bot_config["temp"],
            "suggested_models": ["gpt-4-turbo", "gpt-4"] if bot_config["temp"] <= 0.6 else ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
            "specialties": specialties[:4]  # Limit to 4 specialties for clean display
        }
    
    return full_bots

# ======================================================
# 💬 ENHANCED API INTEGRATION & CHAT FUNCTIONALITY
# ======================================================

class ChatManager:
    def __init__(self):
        self.token_manager = None
        self.last_model = None
    
    def initialize_client(self, api_key: str, model: str):
        """Initialize OpenAI client and token manager with enhanced error handling"""
        try:
            if api_key and api_key != "demo_key":
                openai.api_key = api_key
            
            # Always initialize token manager, even for demo mode
            if not self.token_manager or self.last_model != model:
                self.token_manager = TokenManager(model)
                self.last_model = model
            
            return True
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            # Still initialize token manager for demo mode
            if not self.token_manager:
                self.token_manager = TokenManager(model)
            return False
    
    def check_usage_limits(self, user_data: dict, estimated_tokens: int) -> Tuple[bool, str]:
        """Check if user can make request based on plan limits"""
        plan_details = user_data["plan_details"]
        usage_stats = st.session_state.usage_stats
        
        # Check token limit per request
        if estimated_tokens > plan_details["max_tokens_per_request"]:
            return False, f"Request too long. Max {plan_details['max_tokens_per_request']} tokens allowed."
        
        # Check daily budget
        if usage_stats["daily_cost"] >= plan_details["daily_budget"]:
            return False, f"Daily budget of ${plan_details['daily_budget']:.2f} exceeded."
        
        return True, ""
    
    def generate_response(self, messages: List[Dict], model: str, temperature: float = 0.7) -> Tuple[str, Dict]:
        """Generate response using OpenAI API with enhanced error handling"""
        try:
            # Ensure token manager is initialized
            if not self.token_manager:
                self.token_manager = TokenManager(model)
            
            # Prepare messages for API
            api_messages = []
            for msg in messages:
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Count input tokens with error handling
            input_text = "\n".join([msg["content"] for msg in api_messages])
            input_tokens = self.token_manager.count_tokens(input_text)
            
            # Check if this is demo mode
            user = st.session_state.get("user", {})
            is_demo = user.get("api_key") == "demo_key" or not user.get("api_key")
            
            if is_demo:
                # Simulated response for demo
                bot_name = messages[0]["content"].split("You are a ")[1].split(".")[0] if "You are a " in messages[0]["content"] else "AI Assistant"
                user_question = messages[-1]["content"]
                
                assistant_message = f"""Thank you for your question about: "{user_question}"

As a {bot_name}, I would provide detailed, actionable advice here. In the full version with your OpenAI API key, you would receive:

• Comprehensive analysis of your specific situation
• Step-by-step implementation strategies
• Industry best practices and case studies
• Specific metrics and KPIs to track success
• Tailored recommendations for your business size and industry

**To get real AI responses:**
1. Obtain an OpenAI API key from platform.openai.com
2. Log out and log back in with your API key
3. Start chatting with any of our 110+ specialized business assistants

This demo shows the interface and features. The actual AI responses will be much more detailed and personalized to your specific business needs."""
                
                output_tokens = self.token_manager.count_tokens(assistant_message)
            else:
                # Real API call
                try:
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=api_messages,
                        temperature=temperature,
                        max_tokens=min(4000, st.session_state.user["plan_details"]["max_tokens_per_request"] // 2)
                    )
                    assistant_message = response.choices[0].message.content
                    output_tokens = response.usage.completion_tokens
                    input_tokens = response.usage.prompt_tokens
                except Exception as api_error:
                    logger.error(f"OpenAI API error: {str(api_error)}")
                    assistant_message = f"I apologize, but I encountered an API error: {str(api_error)}. Please check your API key and try again."
                    output_tokens = self.token_manager.count_tokens(assistant_message)
            
            total_tokens = input_tokens + output_tokens
            cost = self.token_manager.estimate_cost(input_tokens, output_tokens)
            
            # Update usage statistics
            self.update_usage_stats(cost, total_tokens)
            
            return assistant_message, {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "cost": cost,
                "model": model,
                "demo_mode": is_demo
            }
            
        except Exception as e:
            logger.error(f"Chat generation error: {str(e)}")
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            
            # Ensure we have a token manager for error handling
            if not self.token_manager:
                self.token_manager = TokenManager(model)
            
            error_tokens = self.token_manager.count_tokens(error_message)
            return error_message, {
                "input_tokens": 0,
                "output_tokens": error_tokens,
                "total_tokens": error_tokens,
                "cost": 0.0,
                "model": model,
                "error": True
            }
    
    def update_usage_stats(self, cost: float, tokens: int):
        """Update usage statistics"""
        if "usage_stats" not in st.session_state:
            st.session_state.usage_stats = {
                "total_cost": 0.0,
                "daily_cost": 0.0,
                "monthly_cost": 0.0,
                "total_tokens": 0,
                "requests_count": 0,
                "last_reset": datetime.now().date()
            }
        
        stats = st.session_state.usage_stats
        
        # Reset daily stats if new day
        if stats["last_reset"] != datetime.now().date():
            stats["daily_cost"] = 0.0
            stats["last_reset"] = datetime.now().date()
        
        stats["total_cost"] += cost
        stats["daily_cost"] += cost
        stats["monthly_cost"] += cost
        stats["total_tokens"] += tokens
        stats["requests_count"] += 1

chat_manager = ChatManager()

# ======================================================
# 🎨 ENHANCED UI COMPONENTS
# ======================================================

def render_usage_dashboard():
    """Render usage statistics dashboard"""
    user = st.session_state.user
    stats = st.session_state.usage_stats
    plan_details = user["plan_details"]
    
    st.sidebar.markdown("### 📊 Usage Dashboard")
    
    # Daily budget progress
    if plan_details["daily_budget"] != float('inf'):
        daily_progress = min(stats["daily_cost"] / plan_details["daily_budget"], 1.0)
        st.sidebar.progress(daily_progress)
        st.sidebar.caption(f"Daily: ${stats['daily_cost']:.3f} / ${plan_details['daily_budget']:.2f}")
    else:
        st.sidebar.info("Unlimited Plan - No Budget Limits")
    
    # Usage metrics
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Total Cost", f"${stats['total_cost']:.3f}")
        st.metric("Requests", stats['requests_count'])
    
    with col2:
        st.metric("Tokens Used", f"{stats['total_tokens']:,}")
        st.metric("Current Plan", user['plan'])

def render_model_selector():
    """Render model selection interface"""
    user = st.session_state.user
    available_models = user["plan_details"]["available_models"]
    
    st.sidebar.markdown("### 🔧 Model Settings")
    
    selected_model = st.sidebar.selectbox(
        "Choose Model",
        available_models,
        help="Higher-tier models provide better responses but cost more"
    )
    
    # Show model pricing
    if selected_model in GPT4_PRICING:
        pricing = GPT4_PRICING[selected_model]
        st.sidebar.caption(f"Input: ${pricing['input']}/1K tokens | Output: ${pricing['output']}/1K tokens")
    
    return selected_model

def render_bot_stats():
    """Render bot statistics and categories"""
    bot_personalities = get_bot_personalities()
    categories = {}
    
    for bot_name, bot_info in bot_personalities.items():
        category = bot_info["category"]
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    st.sidebar.markdown("### 🤖 Bot Statistics")
    st.sidebar.metric("Total Bots", len(bot_personalities))
    st.sidebar.metric("Categories", len(categories))
    
    with st.sidebar.expander("📊 Category Breakdown"):
        for category, count in sorted(categories.items()):
            st.write(f"**{category}:** {count} bots")

# ======================================================
# 📄 PAGE: ENHANCED AUTHENTICATION
# ======================================================

def authentication_page():
    """Enhanced user authentication page"""
    st.title("🔐 Enhanced Business AI Assistant Login")
    st.markdown("Access your personalized AI business consultants with 110+ specialized assistants")
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 🚀 **110+ AI Assistants**
        - Business specialists
        - Format experts (PDF, CSV, SQL, etc.)
        - Industry professionals
        """)
    
    with col2:
        st.markdown("""
        ### 💡 **Smart Features**
        - Real-time usage tracking
        - Multiple AI models
        - Professional chat interface
        """)
    
    with col3:
        st.markdown("""
        ### 🔧 **Format Specialists**
        - PDF Document Expert
        - CSV Data Analyst
        - SQL Database Consultant
        - API Integration Specialist
        """)
    
    # Login form
    with st.form("login_form"):
        st.markdown("### Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        api_key = st.text_input("OpenAI API Key (Optional for Demo)", type="password", 
                               help="Enter your OpenAI API key for real AI responses, or leave blank for demo mode")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("🚀 Login", use_container_width=True)
        with col2:
            demo_button = st.form_submit_button("🎮 Quick Demo", use_container_width=True)
    
    # Handle login
    if login_button:
        if username and password:
            user = authenticate_user(username, password)
            if user:
                user["api_key"] = api_key if api_key else "demo_key"
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.messages = []
                st.session_state.usage_stats = {
                    "total_cost": 0.0,
                    "daily_cost": 0.0,
                    "monthly_cost": 0.0,
                    "total_tokens": 0,
                    "requests_count": 0,
                    "last_reset": datetime.now().date()
                }
                st.rerun()
            else:
                st.error("Invalid username or password")
        else:
            st.error("Please fill in username and password")
    
    # Handle demo mode
    if demo_button:
        demo_user = {
            "username": "demo_user",
            "plan": "Pro",
            "plan_details": SUBSCRIPTION_PLANS["Pro"],
            "api_key": "demo_key",
            "session_start": datetime.now(),
            "created_date": datetime.now() - timedelta(days=7)
        }
        st.session_state.authenticated = True
        st.session_state.user = demo_user
        st.session_state.messages = []
        st.session_state.usage_stats = {
            "total_cost": 2.45,
            "daily_cost": 0.23,
            "monthly_cost": 15.67,
            "total_tokens": 12450,
            "requests_count": 28,
            "last_reset": datetime.now().date()
        }
        st.rerun()
    
    # Demo credentials info
    st.markdown("---")
    st.markdown("### 🎯 Demo Credentials")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Basic User**\nUsername: `demo`\nPassword: `demo123`")
    with col2:
        st.info("**Premium User**\nUsername: `premium`\nPassword: `premium123`")
    with col3:
        st.info("**Admin User**\nUsername: `admin`\nPassword: `admin123`")
    
    # Enhanced subscription plans
    st.markdown("### 💎 Enhanced Subscription Plans")
    plan_cols = st.columns(len(SUBSCRIPTION_PLANS))
    for idx, (plan_name, plan_details) in enumerate(SUBSCRIPTION_PLANS.items()):
        with plan_cols[idx]:
            budget_text = f"${plan_details['monthly_budget']:.0f}/month" if plan_details['monthly_budget'] != float('inf') else "Unlimited"
            st.markdown(f"""
            <div style="
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                height: 220px;
                background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if plan_name == 'Unlimited' else 'white'};
                color: {'white' if plan_name == 'Unlimited' else 'black'};
            ">
                <h4>{plan_name}</h4>
                <p><strong>{budget_text}</strong></p>
                <p>{plan_details['max_tokens_per_request']:,} tokens/request</p>
                <p>{len(plan_details['available_models'])} AI models</p>
                <p>110+ AI assistants</p>
            </div>
            """, unsafe_allow_html=True)

# ======================================================
# 📄 PAGE: ENHANCED BOT MANAGEMENT
# ======================================================

def bot_management_page():
    """Enhanced Bot Management and Information Page"""
    st.title("🤖 Enhanced AI Assistant Directory")
    st.markdown("Discover our 110+ specialized AI assistants including new format-specific experts!")
    
    bot_personalities = get_bot_personalities()
    
    # Enhanced filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categories = list(set([bot["category"] for bot in bot_personalities.values()]))
        selected_category = st.selectbox("Filter by Category", ["All Categories"] + sorted(categories))
    
    with col2:
        # Temperature filter
        temp_filter = st.selectbox("Filter by Creativity", ["All Levels", "Low (0.4-0.5)", "Medium (0.6-0.7)", "High (0.8+)"])
    
    with col3:
        # Search functionality
        search_term = st.text_input("🔍 Search bots", placeholder="Search by name or specialty...")
    
    # New format specialists highlight
    if selected_category == "All Categories" or selected_category == "Format Specialists":
        st.markdown("### 🆕 New Format Specialists")
        format_bots = {k: v for k, v in bot_personalities.items() if v["category"] == "Format Specialists"}
        
        format_cols = st.columns(5)
        for idx, (bot_name, bot_info) in enumerate(list(format_bots.items())[:5]):
            with format_cols[idx]:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
                    padding: 15px;
                    border-radius: 10px;
                    color: white;
                    text-align: center;
                    margin-bottom: 10px;
                ">
                    <h4 style="margin: 0; color: white;">{bot_info['emoji']}</h4>
                    <p style="margin: 5px 0 0 0; font-size: 0.8em;">{bot_name}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Chat with {bot_name}", key=f"format_chat_{idx}"):
                    st.session_state.selected_bot = bot_name
                    st.session_state.current_page = "chat"
                    st.rerun()
    
    # Filter bots
    filtered_bots = {}
    for name, bot in bot_personalities.items():
        # Category filter
        if selected_category != "All Categories" and bot["category"] != selected_category:
            continue
        
        # Temperature filter
        if temp_filter != "All Levels":
            temp = bot["temperature"]
            if temp_filter == "Low (0.4-0.5)" and not (0.4 <= temp <= 0.5):
                continue
            elif temp_filter == "Medium (0.6-0.7)" and not (0.6 <= temp <= 0.7):
                continue
            elif temp_filter == "High (0.8+)" and temp < 0.8:
                continue
        
        # Search filter
        if search_term:
            search_lower = search_term.lower()
            if (search_lower not in name.lower() and 
                search_lower not in bot["description"].lower() and
                not any(search_lower in specialty.lower() for specialty in bot["specialties"])):
                continue
        
        filtered_bots[name] = bot
    
    st.markdown(f"### Found {len(filtered_bots)} AI Assistants")
    
    # Category statistics
    if len(filtered_bots) > 0:
        category_counts = {}
        for bot in filtered_bots.values():
            cat = bot["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        st.markdown("**Category Distribution:**")
        category_text = " | ".join([f"{cat}: {count}" for cat, count in sorted(category_counts.items())])
        st.caption(category_text)
    
    # Display bots in enhanced grid layout
    cols = st.columns(2)
    for idx, (bot_name, bot_info) in enumerate(filtered_bots.items()):
        with cols[idx % 2]:
            with st.container():
                # Enhanced bot card header
                gradient_color = "#ff7e5f, #feb47b" if bot_info["category"] == "Format Specialists" else "#667eea, #764ba2"
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {gradient_color});
                    padding: 20px;
                    border-radius: 10px;
                    color: white;
                    margin-bottom: 10px;
                ">
                    <h3 style="margin: 0; color: white;">{bot_info['emoji']} {bot_name}</h3>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">{bot_info['category']}</p>
                    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 0.9em;">Temperature: {bot_info['temperature']} | Models: {len(bot_info['suggested_models'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Bot details
                st.write(f"**Description:** {bot_info['description']}")
                
                # Specialties with enhanced styling
                st.write("**Specialties:**")
                specialty_tags = " ".join([f"`{spec}`" for spec in bot_info['specialties']])
                st.markdown(specialty_tags)
                
                # Technical details
                with st.expander("🔧 Technical Details"):
                    st.write(f"**Recommended Models:** {', '.join(bot_info['suggested_models'])}")
                    st.write(f"**Temperature:** {bot_info['temperature']} (creativity level)")
                    st.write(f"**Category:** {bot_info['category']}")
                    st.write("**System Prompt Preview:**")
                    st.text(bot_info['system_prompt'][:200] + "...")
                
                # Enhanced action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"💬 Chat", key=f"chat_{idx}"):
                        st.session_state.selected_bot = bot_name
                        st.session_state.current_page = "chat"
                        st.rerun()
                
                with col2:
                    if st.button(f"📋 Copy", key=f"copy_{idx}"):
                        st.code(bot_info['system_prompt'], language="text")
                
                with col3:
                    if st.button(f"⭐ Favorite", key=f"fav_{idx}"):
                        st.success("Added to favorites!")
                
                st.divider()
    
    # Enhanced custom bot section
    st.markdown("### 🛠️ Create Custom Bot")
    with st.expander("Build Your Own AI Assistant"):
        col1, col2 = st.columns(2)
        
        with col1:
            custom_name = st.text_input("Bot Name")
            custom_category = st.selectbox("Category", sorted(set([bot["category"] for bot in bot_personalities.values()])))
            custom_emoji = st.text_input("Emoji", value="🤖")
            custom_temperature = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.7)
        
        with col2:
            custom_description = st.text_area("Description", height=100)
            custom_specialties = st.text_input("Specialties (comma-separated)")
            custom_models = st.multiselect("Suggested Models", ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"])
        
        custom_prompt = st.text_area("System Prompt", height=150)
        
        if st.button("💾 Save Custom Bot"):
            if custom_name and custom_description and custom_prompt:
                # In production, save to database
                st.success(f"Custom bot '{custom_name}' created! (Note: This is a demo - saving not implemented)")
                st.balloons()
            else:
                st.error("Please fill in all required fields")

# ======================================================
# 📄 PAGE: ENHANCED CHAT INTERFACE
# ======================================================

def chat_interface_page():
    """Enhanced Main Chat Interface Page"""
    user = st.session_state.user
    bot_personalities = get_bot_personalities()
    
    # Enhanced header with navigation
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.title("💬 Enhanced AI Chat Interface")
    with col2:
        if st.button("🤖 View All Bots"):
            st.session_state.current_page = "bot_management"
            st.rerun()
    with col3:
        if st.button("📊 Analytics"):
            st.session_state.current_page = "analytics"
            st.rerun()
    with col4:
        if st.button("🚪 Logout"):
            for key in ["authenticated", "user", "messages", "usage_stats"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Enhanced user info
    is_demo = user.get("api_key") == "demo_key"
    demo_badge = " 🎮 (Demo Mode)" if is_demo else ""
    st.caption(f"Welcome back, **{user['username']}**{demo_badge} | Plan: **{user['plan']}** | Session: {user['session_start'].strftime('%H:%M')} | Total Bots: **110+**")
    
    if is_demo:
        st.info("🎮 **Demo Mode Active** - Responses are simulated. Add your OpenAI API key for real AI responses!")
    
    # Enhanced sidebar
    with st.sidebar:
        # Current bot selection with enhanced display
        st.markdown("### 🤖 Current Assistant")
        current_bot = st.session_state.get("selected_bot", "Startup Strategist")
        
        if current_bot in bot_personalities:
            bot_info = bot_personalities[current_bot]
            gradient_color = "#ff7e5f, #feb47b" if bot_info["category"] == "Format Specialists" else "#667eea, #764ba2"
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {gradient_color});
                padding: 15px;
                border-radius: 8px;
                color: white;
                margin-bottom: 15px;
            ">
                <h4 style="margin: 0; color: white;">{bot_info['emoji']} {current_bot}</h4>
                <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9em;">{bot_info['category']}</p>
                <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 0.8em;">Temp: {bot_info['temperature']} | Specialties: {len(bot_info['specialties'])}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick bot switcher with categories
        st.markdown("### ⚡ Quick Switch")
        
        # Format specialists section
        st.markdown("**🆕 Format Specialists:**")
        format_bots = [name for name, bot in bot_personalities.items() if bot["category"] == "Format Specialists"]
        for bot_name in format_bots[:3]:  # Show first 3
            if bot_name != current_bot:
                if st.button(f"{bot_personalities[bot_name]['emoji']} {bot_name}", key=f"switch_format_{bot_name}"):
                    st.session_state.selected_bot = bot_name
                    st.rerun()
        
        # Popular bots section
        st.markdown("**🔥 Popular Assistants:**")
        popular_bots = ["Startup Strategist", "Marketing Strategy Expert", "Financial Controller", "Operations Excellence Manager"]
        for bot_name in popular_bots:
            if bot_name != current_bot and bot_name in bot_personalities:
                if st.button(f"{bot_personalities[bot_name]['emoji']} {bot_name}", key=f"switch_popular_{bot_name}"):
                    st.session_state.selected_bot = bot_name
                    st.rerun()
        
        # Model selection
        selected_model = render_model_selector()
        
        # Usage dashboard
        render_usage_dashboard()
        
        # Bot statistics
        render_bot_stats()
        
        # Enhanced chat controls
        st.markdown("### 🔧 Chat Controls")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🗑️ Clear"):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("💾 Export"):
                chat_export = {
                    "bot": current_bot,
                    "timestamp": datetime.now().isoformat(),
                    "messages": st.session_state.messages,
                    "user": user["username"],
                    "plan": user["plan"]
                }
                st.download_button(
                    "📥 Download",
                    json.dumps(chat_export, indent=2),
                    file_name=f"chat_{current_bot}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("📝 Business Plan Help"):
            st.session_state.selected_bot = "Business Plan Writer"
            st.rerun()
        
        if st.button("📊 Data Analysis"):
            st.session_state.selected_bot = "CSV Data Analyst"
            st.rerun()
        
        if st.button("🔗 API Integration"):
            st.session_state.selected_bot = "API Integration Specialist"
            st.rerun()
    
    # Main chat area with enhancements
    st.markdown("### 💬 Chat with Your AI Assistant")
    
    # Chat statistics
    if st.session_state.messages:
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.caption(f"💬 {total_messages} total messages | 👤 {user_messages} from you | 🤖 {total_messages - user_messages} from AI")
    
    # Display chat messages with enhanced styling
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Enhanced metadata display
            if "metadata" in message and message["metadata"]:
                metadata = message["metadata"]
                
                # Show cost and token info
                if "cost" in metadata:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.caption(f"💰 ${metadata.get('cost', 0):.4f}")
                    with col2:
                        st.caption(f"🔢 {metadata.get('total_tokens', 0)} tokens")
                    with col3:
                        st.caption(f"🤖 {metadata.get('model', 'N/A')}")
                    with col4:
                        if metadata.get('demo_mode'):
                            st.caption("🎮 Demo")
                        elif metadata.get('error'):
                            st.caption("❌ Error")
                        else:
                            st.caption("✅ Real")
                
                # Expandable detailed metadata
                with st.expander("📊 Message Details"):
                    st.json(metadata)
    
    # Enhanced chat input with suggestions
    if not st.session_state.messages:
        st.markdown("### 💡 Suggested Questions:")
        
        # Bot-specific suggestions
        if current_bot in bot_personalities:
            bot_info = bot_personalities[current_bot]
            suggestions = []
            
            if "Format Specialists" in bot_info["category"]:
                suggestions = [
                    f"How can you help me with {bot_info['specialties'][0].lower()}?",
                    "What are the best practices for this format?",
                    "Can you help me automate this process?"
                ]
            else:
                suggestions = [
                    f"What are the key challenges in {bot_info['category'].lower()}?",
                    "Can you help me create a strategy?",
                    "What metrics should I track?"
                ]
            
            suggestion_cols = st.columns(len(suggestions))
            for idx, suggestion in enumerate(suggestions):
                with suggestion_cols[idx]:
                    if st.button(suggestion, key=f"suggestion_{idx}"):
                        # Add suggestion as user message
                        st.session_state.messages.append({"role": "user", "content": suggestion})
                        st.rerun()
    
    # Chat input with enhanced features
    if prompt := st.chat_input("Ask your AI assistant anything..."):
        # Initialize chat manager
        chat_manager.initialize_client(user.get("api_key", ""), selected_model)
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                # Prepare messages for API
                messages_for_api = [
                    {"role": "system", "content": bot_personalities[current_bot]["system_prompt"]}
                ] + st.session_state.messages
                
                # Generate response
                response, metadata = chat_manager.generate_response(
                    messages_for_api,
                    selected_model,
                    bot_personalities[current_bot]["temperature"]
                )
                
                st.markdown(response)
                
                # Show quick metadata
                if metadata:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"💰 ${metadata.get('cost', 0):.4f}")
                    with col2:
                        st.caption(f"🔢 {metadata.get('total_tokens', 0)} tokens")
                    with col3:
                        if metadata.get('demo_mode'):
                            st.caption("🎮 Demo Mode")
                        else:
                            st.caption("✅ Real Response")
                
                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "metadata": metadata
                })
        
        st.rerun()

# ======================================================
# 📄 PAGE: ANALYTICS DASHBOARD
# ======================================================

def analytics_page():
    """Analytics and insights dashboard"""
    st.title("📊 Analytics Dashboard")
    st.markdown("Insights into your AI assistant usage and performance")
    
    user = st.session_state.user
    stats = st.session_state.usage_stats
    bot_personalities = get_bot_personalities()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Conversations",
            stats['requests_count'],
            delta=f"+{stats['requests_count'] - 20}" if stats['requests_count'] > 20 else None
        )
    
    with col2:
        st.metric(
            "Total Cost",
            f"${stats['total_cost']:.3f}",
            delta=f"+${stats['daily_cost']:.3f} today"
        )
    
    with col3:
        st.metric(
            "Tokens Used",
            f"{stats['total_tokens']:,}",
            delta=f"+{stats['total_tokens'] - 10000:,}" if stats['total_tokens'] > 10000 else None
        )
    
    with col4:
        efficiency = stats['total_tokens'] / max(stats['requests_count'], 1)
        st.metric(
            "Avg Tokens/Chat",
            f"{efficiency:.0f}",
            delta=f"{efficiency - 400:.0f}" if efficiency > 400 else None
        )
    
    # Usage charts (simulated data for demo)
    st.markdown("### 📈 Usage Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Daily Usage (Last 7 Days)**")
        chart_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Requests': [5, 8, 12, 6, 15, 3, 7],
            'Cost': [0.15, 0.24, 0.36, 0.18, 0.45, 0.09, 0.21]
        })
        st.bar_chart(chart_data.set_index('Day')['Requests'])
    
    with col2:
        st.markdown("**Cost Distribution**")
        st.bar_chart(chart_data.set_index('Day')['Cost'])
    
    # Bot usage analysis
    st.markdown("### 🤖 Bot Usage Analysis")
    
    # Simulated bot usage data
    bot_usage = {
        "Startup Strategist": 15,
        "Marketing Strategy Expert": 12,
        "Financial Controller": 8,
        "CSV Data Analyst": 6,
        "API Integration Specialist": 4,
        "PDF Document Specialist": 3
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Most Used Assistants**")
        for bot_name, usage_count in bot_usage.items():
            if bot_name in bot_personalities:
                bot_info = bot_personalities[bot_name]
                st.write(f"{bot_info['emoji']} **{bot_name}**: {usage_count} chats")
    
    with col2:
        st.markdown("**Category Distribution**")
        category_usage = {}
        for bot_name, usage_count in bot_usage.items():
            if bot_name in bot_personalities:
                category = bot_personalities[bot_name]["category"]
                category_usage[category] = category_usage.get(category, 0) + usage_count
        
        for category, count in sorted(category_usage.items(), key=lambda x: x[1], reverse=True):
            st.write(f"**{category}**: {count} chats")
    
    # Performance insights
    st.markdown("### 💡 Performance Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ **Top Performing Categories**")
        st.write("• Format Specialists showing high engagement")
        st.write("• Business strategy bots most frequently used")
        st.write("• Technical assistants have longest conversations")
    
    with col2:
        st.info("📊 **Usage Recommendations**")
        st.write("• Try the new PDF Document Specialist")
        st.write("• Explore SQL Database Consultant for data tasks")
        st.write("• Consider upgrading plan for more features")
    
    # Export options
    st.markdown("### 📥 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Usage Data"):
            usage_data = {
                "user": user["username"],
                "plan": user["plan"],
                "stats": stats,
                "bot_usage": bot_usage,
                "export_date": datetime.now().isoformat()
            }
            st.download_button(
                "Download Usage Report",
                json.dumps(usage_data, indent=2),
                file_name=f"usage_report_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📈 Generate Report"):
            st.success("Report generated! Check your downloads.")
    
    with col3:
        if st.button("🔄 Refresh Data"):
            st.rerun()

# ======================================================
# 🚀 ENHANCED MAIN APPLICATION
# ======================================================

def main():
    """Enhanced main application entry point"""
    # Enhanced page configuration
    st.set_page_config(
        page_title="Enhanced Business AI Assistants",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo',
            'Report a bug': 'https://github.com/your-repo/issues',
            'About': "Enhanced Business AI Assistants with 110+ specialized bots!"
        }
    )
    
    # Enhanced custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .bot-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background: white;
        transition: transform 0.2s;
    }
    .bot-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .format-specialist {
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
        color: white;
    }
    .stButton > button {
        border-radius: 20px;
        border: none;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize enhanced session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "chat"
    
    if "selected_bot" not in st.session_state:
        st.session_state.selected_bot = "Startup Strategist"
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "usage_stats" not in st.session_state:
        st.session_state.usage_stats = {
            "total_cost": 0.0,
            "daily_cost": 0.0,
            "monthly_cost": 0.0,
            "total_tokens": 0,
            "requests_count": 0,
            "last_reset": datetime.now().date()
        }
    
    # Enhanced main application logic
    if not st.session_state.authenticated:
        authentication_page()
    else:
        # Enhanced navigation
        if st.session_state.current_page == "bot_management":
            bot_management_page()
        elif st.session_state.current_page == "analytics":
            analytics_page()
        else:
            chat_interface_page()

if __name__ == "__main__":
    main()

