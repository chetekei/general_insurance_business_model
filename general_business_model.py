import streamlit as st
import pandas as pd

first_tab = pd.DataFrame()
second_tab = pd.DataFrame()

st.header('GENERAL BUSINESS MARKETING MODEL')

tab1, tab2, tab3 = st.tabs(["Parameters" ,"📈 Met Targets",  "📈 Surpassed Target"])

with tab1:    
    bd_executives = int(st.number_input('Number of Business Development Executives'))    
    agents = int(st.number_input('Number of Agents Per Team Leader'))
    months = int(st.number_input('Number of Months'))
    monthly_sales = int(st.number_input('Monthly Production Per Agent'))
    commission = st.number_input('Commission for Business Brought Up to 100,000')
    monthly_salary = st.number_input('Monthly Salary for Business Development Executives')
    success_agents = st.number_input('Percentage Of Agents Who Exceeded The Target')
    success_rate = st.number_input('Exceeded Target by X Percentage')
    bonus_commission = st.number_input('Commission Bonus on Exceeded Target')

    if st.button("Calculate"):
        def calculate_cashflow(months):
            results = []
            newresults = []

            for month in range(1, months + 1):
                aggregate_income = round(bd_executives * agents * monthly_sales)
                salary = round(bd_executives * monthly_salary)
                commission_payable = round(aggregate_income * (commission/100))
                total_expenses = round(salary + commission)
                exceeded = round(bd_executives * (agents * (1 + (success_agents/100))) * (monthly_sales * (1 + (success_rate/100))))
                new_commission_payable = round((monthly_sales * (commission/100)) + ((exceeded - aggregate_income) * bonus_commission))
                new_total_expenses = round(salary + new_commission_payable)
                net_income = round(aggregate_income - total_expenses)
                new_net_income = round(exceeded - new_total_expenses)

                results.append({
                    'Month': f'Month {month}',
                    'Aggregate Income': aggregate_income,
                    'Monthly Salary': salary,
                    'Total Commission': commission_payable,
                    'Total Expenses': total_expenses,
                    'Net Income': net_income})
                
                newresults.append({
                    'Month': f'Month {month}',
                    'Aggregate Income': exceeded,
                    'Monthly Salary': salary,
                    'Total Commission': new_commission_payable,
                    'Total Expenses': new_total_expenses,
                    'Net Income': new_net_income})

            # Add a row for totals
            total_row = {
                'Month': 'Total',
                'Aggregate Income': round(sum(item['Aggregate Income'] for item in results)),
                'Monthly Salary': round(sum(item['Monthly Salary'] for item in results)),
                'Total Commission': round(sum(item['Total Commission'] for item in results)),
                'Total Expenses': round(sum(item['Total Expenses'] for item in results)),
                'Net Income': round(sum(item['Net Income'] for item in results))
            }
            results.append(total_row)

            total_row_new = {
                'Month': 'Total',
                'Aggregate Income': round(sum(item['Aggregate Income'] for item in newresults)),
                'Monthly Salary': round(sum(item['Monthly Salary'] for item in newresults)),
                'Total Commission': round(sum(item['Total Commission'] for item in newresults)),
                'Total Expenses': round(sum(item['Total Expenses'] for item in newresults)),
                'Net Income': round(sum(item['Net Income'] for item in results))
            }
            newresults.append(total_row_new)

            return results, newresults

        results, newresults = calculate_cashflow(months)

        first_tab = pd.DataFrame(results)
        second_tab = pd.DataFrame(newresults)

    

with tab2:
    if not first_tab.empty:
        st.table(first_tab)

with tab3:
    if not second_tab.empty:
        st.table(second_tab)

