# -*- coding: utf-8 -*-

"""
This module contains Django models for the OEB Open Data application(s).

Ontario's Digital and Data Directive ensures the delivery of high-quality digital services and access to public government data, 
unless it is exempt for legal, privacy, security, confidentiality or commercially-sensitive reasons. The directive sets out key 
principles and requirements for the design of digital services and the sharing of open government data assets.

These tables are built from the xml files provided by the Ontario Energy Board (OEB) and are used to store the data in a structured
format. The data is then used to generate reports and visualizations for the OEB Open Data application.

https://www.oeb.ca/open-data

Version: 1.0.0

Change Log:
- 1.0.0 (2022-01-01): Initial version of the models.
"""

from django.db import models


class GApplication(models.Model):
    """
    Represents a GApplication object - which is the applications
    before the various regulatory boards

    https://www.oeb.ca/open-data/applications-oeb

    Attributes:
        application1 (str): The first application.
        date_filed1 (date): The date the application was filed.
        energy_type1 (str): The type of energy.
        category1 (str): The category of the application.
        applicant1 (str): The applicant of the application.
        reg_case_status (str): The status of the registered case.
        application_name (str): The name of the application.
        process_type (str): The type of process.
        case_authority (str): The authority handling the case.
        case_status (str): The status of the case.
    """

    application = models.CharField(max_length=255)
    date_filed = models.DateField()
    energy_type = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    applicant = models.CharField(max_length=255)
    reg_case_status = models.CharField(max_length=255)
    application_name = models.CharField(max_length=255)
    process_type = models.CharField(max_length=255)
    case_authority = models.CharField(max_length=255)
    case_status = models.CharField(max_length=255)


class ResCurrElecRates(models.Model):
    """
    Model representing the current electricity rates for residential customers.

    https://www.oeb.ca/open-data/current-electricity-rates-residential-rate-class

    Attributes:
        dist (str): The name of the distribution company.
        class_name (str): The name of the electricity rate class.
        year (int): The year for which the rates are applicable.
        et1 (float): The energy tier 1 rate.
        rpp1 (float): The RPP tier 1 rate.
        rpp2 (float): The RPP tier 2 rate.
        sc (float): The supply charge rate.
        dc (float): The delivery charge rate.
        ga_rr_nonrpp (float): The GA RR non-RPP rate.
        net (float): The net rate.
        conn (float): The connection rate.
        wmsr (float): The WMSR rate.
        rrrp (float): The RRRP rate.
        sss (float): The SSS rate.
        lf (float): The LF rate.
        gst (float): The GST rate.
        eoffp (float): The EOFFP rate.
        emidp (float): The EMIDP rate.
        eonp (float): The EONP rate.
        rppoffp (float): The RPPOFFP rate.
        rppmidp (float): The RPPMIDP rate.
        rpponp (float): The RPPOONP rate.
        pbga (float): The PBGA rate.
        rebate (float): The rebate rate.
        ofc (float): The OFC rate.
        vc (float): The VC rate.
        oc (float): The OC rate.
        drp (float): The DRP rate.
        drc (str): The DRC rate.
        drp_rate (float): The DRP rate.
        ulo_midp (float): The ULO MIDP rate.
        ulo_midp_period (float): The ULO MIDP period rate.
        ulo_onp (float): The ULO ONP rate.
        ulo_onp_period (float): The ULO ONP period rate.
        ulo_overnight (float): The ULO overnight rate.
        ulo_overnight_period (float): The ULO overnight period rate.
        ulo_weekendoffp (float): The ULO weekend off-peak rate.
        ulo_weekendoffp_period (float): The ULO weekend off-peak period rate.
    """

    dist = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)
    year = models.IntegerField()
    et1 = models.FloatField()
    rpp1 = models.FloatField()
    rpp2 = models.FloatField()
    sc = models.FloatField()
    dc = models.FloatField()
    ga_rr_nonrpp = models.FloatField()
    net = models.FloatField()
    conn = models.FloatField()
    wmsr = models.FloatField()
    rrrp = models.FloatField()
    sss = models.FloatField()
    lf = models.FloatField()
    gst = models.FloatField()
    eoffp = models.FloatField()
    emidp = models.FloatField()
    eonp = models.FloatField()
    rppoffp = models.FloatField()
    rppmidp = models.FloatField()
    rpponp = models.FloatField()
    pbga = models.FloatField()
    rebate = models.FloatField()
    ofc = models.FloatField()
    vc = models.FloatField(null=True, blank=True)
    oc = models.FloatField()
    drp = models.FloatField()
    drc = models.CharField(max_length=255, null=True, blank=True)
    drp_rate = models.FloatField()
    ulo_midp = models.FloatField()
    ulo_midp_period = models.FloatField()
    ulo_onp = models.FloatField()
    ulo_onp_period = models.FloatField()
    ulo_overnight = models.FloatField()
    ulo_overnight_period = models.FloatField()
    ulo_weekendoffp = models.FloatField()
    ulo_weekendoffp_period = models.FloatField()


class MMCurrElecRates(models.Model):
    """
    Model representing the current electricity rates for a specific distribution company.

    https://www.oeb.ca/open-data/current-electricity-rates-general-service-50-kw-rate-class

    Attributes:
        dist (str): The name of the distribution company.
        class_name (str): The name of the electricity rate class.
        year (int): The year for which the rates are applicable.
        et1 (float): The energy tier 1 rate.
        rpp1 (float): The RPP tier 1 rate.
        rpp2 (float): The RPP tier 2 rate.
        sc (float): The supply charge rate.
        dc (float): The delivery charge rate.
        ga_rr_nonrpp (float): The GA RR non-RPP rate.
        net (float): The net rate.
        conn (float): The connection rate.
        wmsr (float): The WMSR rate.
        rrrp (float): The RRRP rate.
        sss (float): The SSS rate.
        lf (float): The LF rate.
        gst (float): The GST rate.
        eoffp (float): The EOFFP rate.
        emidp (float): The EMIDP rate.
        eonp (float): The EONP rate.
        rppoffp (float): The RPPOFFP rate.
        rppmidp (float): The RPPMIDP rate.
        rpponp (float): The RPPOONP rate.
        pbga (float): The PBGA rate.
        rebate (float): The rebate rate.
        ofc (float): The OFC rate.
        vc (float): The VC rate.
        oc (float): The OC rate.
        drp (float): The DRP rate.
        drc (str): The DRC rate.
        drp_rate (float): The DRP rate.
        ulo_midp (float): The ULO MIDP rate.
        ulo_midp_period (float): The ULO MIDP period rate.
        ulo_onp (float): The ULO ONP rate.
        ulo_onp_period (float): The ULO ONP period rate.
        ulo_overnight (float): The ULO overnight rate.
        ulo_overnight_period (float): The ULO overnight period rate.
        ulo_weekendoffp (float): The ULO weekend off-peak rate.
        ulo_weekendoffp_period (float): The ULO weekend off-peak period rate.
    """

    dist = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)
    year = models.IntegerField()
    et1 = models.FloatField()
    rpp1 = models.FloatField()
    rpp2 = models.FloatField()
    sc = models.FloatField()
    dc = models.FloatField()
    ga_rr_nonrpp = models.FloatField()
    net = models.FloatField()
    conn = models.FloatField()
    wmsr = models.FloatField()
    rrrp = models.FloatField()
    sss = models.FloatField()
    lf = models.FloatField()
    gst = models.FloatField()
    eoffp = models.FloatField()
    emidp = models.FloatField()
    eonp = models.FloatField()
    rppoffp = models.FloatField()
    rppmidp = models.FloatField()
    rpponp = models.FloatField()
    pbga = models.FloatField()
    rebate = models.FloatField()
    ofc = models.FloatField()
    vc = models.FloatField()
    oc = models.FloatField()
    drp = models.FloatField()
    drc = models.CharField(max_length=255)
    drp_rate = models.FloatField()
    ulo_midp = models.FloatField()
    ulo_midp_period = models.FloatField()
    ulo_onp = models.FloatField()
    ulo_onp_period = models.FloatField()
    ulo_overnight = models.FloatField()
    ulo_overnight_period = models.FloatField()
    ulo_weekendoffp = models.FloatField()
    ulo_weekendoffp_period = models.FloatField()


class ResCurrGasRates(models.Model):
    """
    Model representing the current gas rates for residential customers.

    https://www.oeb.ca/open-data/current-natural-gas-rates-residential-rate-classes

    Attributes:
        lic (int): The license number.
        ext_id (int): The external ID.
        dist (str): The name of the distribution company.
        sa (str): The service area.
        rc (int): The rate class.
        ed (datetime): The effective date.
        mc (float): The monthly charge.
        dt1_low (int): The low range for tier 1.
        dt1_high (int): The high range for tier 1.
        dt2_low (int): The low range for tier 2.
        dt2_high (int): The high range for tier 2.
        dt3_low (int): The low range for tier 3.
        dt3_high (int): The high range for tier 3.
        dt4_low (int): The low range for tier 4.
        dt4_high (int): The high range for tier 4.
        dt5_low (int): The low range for tier 5.
        dt5_high (int): The high range for tier 5.
        dct1 (float): The delivery charge rate for tier 1.
        dct2 (float): The delivery charge rate for tier 2.
        dct3 (float): The delivery charge rate for tier 3.
        dct4 (float): The delivery charge rate for tier 4.
        dct5 (float): The delivery charge rate for tier 5.
        dcpa (float): The delivery charge per adjustment.
        sc (float): The storage charge.
        scpa (float): The storage charge per adjustment.
        cm (float): The commodity charge.
        cmpa (float): The commodity charge per adjustment.
        tc (float): The transportation charge.
        tcpa (float): The transportation charge per adjustment.
        fed_cc (float): The federal carbon charge.
        fac_cc (float): The facility carbon charge.
        gst (float): The GST rate.
        jan (int): The January consumption.
        feb (int): The February consumption.
        mar (int): The March consumption.
        apr (int): The April consumption.
        may (int): The May consumption.
        jun (int): The June consumption.
        jul (int): The July consumption.
        aug (int): The August consumption.
        sep (int): The September consumption.
        oct (int): The October consumption.
        nov (int): The November consumption.
        dec (int): The December consumption.
    """

    lic = models.IntegerField()
    ext_id = models.IntegerField()
    dist = models.CharField(max_length=255)
    sa = models.CharField(max_length=255)
    rc = models.IntegerField()
    ed = models.DateTimeField()
    mc = models.FloatField()
    dt1_low = models.IntegerField()
    dt1_high = models.IntegerField()
    dt2_low = models.IntegerField()
    dt2_high = models.IntegerField()
    dt3_low = models.IntegerField()
    dt3_high = models.IntegerField()
    dt4_low = models.IntegerField()
    dt4_high = models.IntegerField()
    dt5_low = models.IntegerField()
    dt5_high = models.IntegerField()
    dct1 = models.FloatField()
    dct2 = models.FloatField()
    dct3 = models.FloatField()
    dct4 = models.FloatField()
    dct5 = models.FloatField()
    dcpa = models.FloatField()
    sc = models.FloatField()
    scpa = models.FloatField()
    cm = models.FloatField()
    cmpa = models.FloatField()
    tc = models.FloatField()
    tcpa = models.FloatField()
    fed_cc = models.FloatField()
    fac_cc = models.FloatField()
    gst = models.FloatField()
    jan = models.IntegerField()
    feb = models.IntegerField()
    mar = models.IntegerField()
    apr = models.IntegerField()
    may = models.IntegerField()
    jun = models.IntegerField()
    jul = models.IntegerField()
    aug = models.IntegerField()
    sep = models.IntegerField()
    oct = models.IntegerField()
    nov = models.IntegerField()
    dec = models.IntegerField()


class DistElectComplaints(models.Model):
    """
    Model representing the distribution electricity complaints.

    https://www.oeb.ca/open-data/electricity-distributor-complaints-received-oeb

    Attributes:
        year (int): The year of the complaints.
        dist (str): The name of the distribution company.
        total (int): The total number of complaints.
    """

    year = models.IntegerField()
    dist = models.CharField(max_length=255)
    total = models.IntegerField()


class DistElecScoreCard(models.Model):
    """
    Represents a scorecard for a distribution electric company.

    Attributes:
        dist (str): The name of the distribution company.
        year (int): The year of the scorecard.
        connections (float): The number of connections.
        appointments (float): The number of appointments.
        tele (float): The telecommunication score.
        billacc (float): The billing accuracy score.
        firstcont (float): The first contact resolution score.
        custsurvey (float): The customer survey score.
        publicawareness (float): The public awareness score.
        ontreg (str): The Ontario regulation.
        genincidents (int): The number of general incidents.
        rateperkm (float): The rate per kilometer.
        powerouttimes (float): The power outage times.
        powerouthrs (float): The power outage hours.
        distplan (float): The distribution plan score.
        efficiency (int): The efficiency score.
        costpercust (int): The cost per customer.
        costperkm (int): The cost per kilometer.
        genconn (str): The general connection.
        genfac (float): The general facility score.
        liquidity (float): The liquidity score.
        leverage (float): The leverage score.
        profitdeemed (float): The deemed profit score.
        profitachieved (float): The achieved profit score.
    """

    dist = models.CharField(max_length=255)
    year = models.IntegerField()
    connections = models.FloatField()
    appointments = models.FloatField()
    tele = models.FloatField()
    billacc = models.FloatField()
    firstcont = models.FloatField()
    custsurvey = models.FloatField()
    publicawareness = models.FloatField()
    ontreg = models.CharField(max_length=255)
    genincidents = models.IntegerField()
    rateperkm = models.FloatField()
    powerouttimes = models.FloatField()
    powerouthrs = models.FloatField()
    distplan = models.FloatField()
    efficiency = models.IntegerField()
    costpercust = models.IntegerField()
    costperkm = models.IntegerField()
    genconn = models.CharField(max_length=255)
    genfac = models.FloatField()
    liquidity = models.FloatField()
    leverage = models.FloatField()
    profitdeemed = models.FloatField()
    profitachieved = models.FloatField()


class LEAP(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    number_of_distributor_customer_leap_applicants = models.IntegerField()
    number_of_unit_sub_metered_leap_applicants = models.IntegerField()
    total_number_of_leap_applicants = models.IntegerField()
    number_of_distributor_customer_applicants_assisted = models.IntegerField()
    number_of_unit_sub_metered_applicants_assisted = models.IntegerField()
    total_number_of_applicants_assisted = models.IntegerField()
    number_of_distributor_customer_applicants_denied = models.IntegerField()
    number_of_unit_sub_metered_applicants_denied = models.IntegerField()
    total_number_of_applicants_denied = models.IntegerField()
    avg_grant_per_assisted_dist_cust_appl_in_dollars = models.FloatField()
    avg_grant_per_assisted_unit_sub_metered_appl_in_dollars = models.FloatField()
    overall_avg_grant_per_assisted_appl_in_dollars = models.FloatField()
    number_of_repeat_distributor_customers = models.IntegerField(null=True)
    number_of_repeat_unit_sub_metered_customers = models.IntegerField(null=True)
    total_number_of_repeat_customers = models.IntegerField()
    funds_received_from_distributor_customers = models.FloatField()
    funds_received_from_unused_funds_from_prev_year = models.FloatField()
    funds_received_from_donations_non_rate_based_sources = models.FloatField()
    funds_received_from_suppl_from_cost_assessment_offset = models.FloatField(null=True)
    total_funds_received_in_dollars = models.FloatField()
    funds_disbursed_for_agency_fees_admin_and_delivery = models.FloatField()
    funds_disbursed_for_distributor_customer_grants = models.FloatField()
    funds_disbursed_for_unit_sub_metered_grants = models.FloatField()
    total_funds_disbursed_for_grants = models.FloatField()
    total_funds_disbursed_in_dollars = models.FloatField()
    unused_funds_at_year_end_in_dollars = models.FloatField()
    recoverable_donations_leap_funding = models.FloatField()
    funding_approved_in_cos_decision = models.FloatField()
    calculated_leap_funding_board_approved = models.FloatField()


class BillingAccuracy(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    asset_management_progress = models.FloatField()
    billing_accuracy_percentage = models.FloatField()
    customer_satisfaction_survey_percentage = models.FloatField()
    first_contact_resolution_percentage = models.FloatField()
    total_number_of_bills_issued_annually = models.IntegerField()
    level_of_compliance_with_ontario_regulation = models.CharField(max_length=255)
    level_of_public_awareness = models.FloatField()
    number_of_general_public_incidents = models.IntegerField()
    rate_category = models.IntegerField()
    rate_per_km_of_line = models.FloatField()


class MarketMonitoring(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    customer_or_connections = models.CharField(max_length=255)
    generic_rate_class = models.CharField(max_length=255)
    detailed_rate_class = models.CharField(max_length=255)
    total_customers_or_connections = models.IntegerField()


class ServiceQuality(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    connections_low_voltage_new_services_within_time = models.IntegerField()
    connections_low_voltage_new_services = models.IntegerField()
    low_voltage_connections_percentage = models.FloatField()
    connections_high_voltage_new_services_within_time = models.IntegerField()
    connections_high_voltage_new_services = models.IntegerField()
    high_voltage_connections_percentage = models.FloatField()
    telephone_accessibility_answered_within_time = models.IntegerField()
    telephone_accessibility_incoming = models.IntegerField()
    telephone_accessibility_percentage = models.FloatField()
    appointments_met_scheduled = models.FloatField()
    appointments_met_completed_as_required = models.IntegerField()
    appointments_met_percentage = models.FloatField()
    written_responses_provided_within_time = models.IntegerField()
    written_responses_received = models.IntegerField()
    written_response_to_enquiries_percentage = models.FloatField()
    emergency_response_urban_call_response_within_time = models.FloatField()
    emergency_response_urban_calls = models.FloatField()
    emergency_urban_response_percentage = models.FloatField()
    emergency_response_rural_call_response_within_time = models.FloatField()
    emergency_response_rural_calls = models.FloatField()
    emergency_rural_response_percentage = models.FloatField(null=True)
    telephone_call_abandon_rate_answered_within_time = models.IntegerField()
    telephone_call_abandon_rate_incoming = models.IntegerField()
    telephone_call_abandon_rate_percentage = models.FloatField()
    appointments_scheduled_scheduled = models.IntegerField()
    appointments_scheduled_requests = models.IntegerField()
    appointments_scheduling_percentage = models.FloatField()
    appointments_rescheduled = models.FloatField()
    appointments_rescheduled_in_time = models.FloatField()
    rescheduling_a_missed_appointment_percentage = models.FloatField()
    reconnections_completed_within_time = models.IntegerField()
    reconnections_total = models.IntegerField()
    reconnection_performance_standards_percentage = models.FloatField()
    micro_embedded_generation_met = models.IntegerField()
    micro_embedded_generation_new = models.IntegerField()
    new_micro_embedded_generation_facilities_connected_percentage = models.FloatField()


class SystemReliability(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.FloatField()
    cause_code = models.FloatField()
    cause_of_interruption = models.CharField(max_length=255)
    average_number_of_customers_served = models.FloatField()
    number_of_interruptions_from_major_events = models.FloatField()
    number_of_customer_interruptions_from_major_events = models.FloatField()
    number_of_customer_hours_of_interruptions_from_major_events = models.FloatField()
    saifi_from_major_events = models.FloatField()
    saidi_from_major_events = models.FloatField()
    number_of_interruptions_from_non_major_events = models.FloatField()
    number_of_customer_interruptions_from_non_major_events = models.FloatField()
    number_of_customer_hours_of_interruptions_from_non_major_events = (
        models.FloatField()
    )
    saifi_from_non_major_events = models.FloatField()
    saidi_from_non_major_events = models.FloatField()
    total_number_of_interruptions = models.FloatField()
    total_number_of_customer_interruptions = models.FloatField()
    total_number_of_customer_hours_of_interruptions = models.FloatField()
    total_saifi = models.FloatField()
    total_saidi = models.FloatField()


class MajorEventResponse(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    submitted_on = models.DateTimeField()
    event_date = models.DateTimeField()
    prior_to_the_major_event_prior_distributor_warning = models.CharField(
        max_length=255
    )
    event_time = models.CharField(max_length=255)
    prior_to_the_major_event_prior_distributor_warning_details = models.CharField(
        max_length=255
    )
    extra_employees_on_duty_and_standby = models.CharField(max_length=255)
    extra_employees_or_employees_were_not_arranged = models.CharField(max_length=255)
    staff_trained_on_the_response_plan = models.CharField(max_length=255)
    media_announcements_to_public_warning_of_possible_outages = models.CharField(
        max_length=255
    )
    was_ieee_standard_use_to_derive_any_threshold = models.CharField(max_length=255)
    estimated_time_of_restoration_issued_to_public = models.CharField(max_length=255)
    estimated_time_of_restoration_issued_to_details = models.TextField()
    number_of_customers_interrupted = models.CharField(max_length=255)
    percentage_of_total_customers_base_interrupted = models.CharField(max_length=255)
    hours_to_restore_ninety_percentage_of_the_customers = models.CharField(
        max_length=255
    )
    hours_to_restore_ninety_percentage_of_the_customers_comments = models.TextField()
    outages_associated_with_loss_of_supply = models.CharField(max_length=255)
    third_party_mutual_assistance_with_other_utilities_details = models.CharField(
        max_length=255
    )
    third_party_mutual_assistance_with_other_utilities = models.CharField(
        max_length=255
    )
    after_mitigation_future_actions = models.TextField()
    need_equipment_or_materials = models.CharField(max_length=255)


class Labour(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.FloatField()
    number_of_full_time_equivalent_employees = models.FloatField()
    number_of_employees_charged_to_om_and_admin = models.FloatField()
    number_of_employees_charged_to_new_construction = models.FloatField()
    salaries_and_wages_paid_to_oma_and_admin_employees = models.FloatField()
    salaries_and_wages_paid_to_new_construction_employees = models.FloatField()


class Capital(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    total_gross_capital_additions = models.FloatField()
    total_retirements_write_offs_sales_asset_impairment_losses = models.FloatField()
    total_contributed_capital = models.FloatField()
    other_changes_to_total_gross_capital = models.FloatField()
    high_voltage_gross_capital_additions = models.FloatField()
    high_voltage_retirements_write_offs_impairment_losses = models.FloatField()
    high_voltage_contributed_capital = models.FloatField()
    other_changes_to_high_voltage_gross_capital = models.FloatField()
    capital_expenditure_direct_labour = models.FloatField()
    capital_expenditure_equipment_and_materials = models.FloatField()
    capital_expenditure_capitalized_overhead = models.FloatField()
    capital_expenditure_contract_services = models.FloatField()
    capital_expenditure_other = models.FloatField()
    intangible_assets_high_voltage_gross_capital_add = models.FloatField(null=True)
    intangible_assets_high_voltage_distributor_contrib_capital = models.FloatField(
        null=True
    )
    intangible_assets_high_voltage_retirements_write_offs = models.FloatField(null=True)
    intangible_assets_high_voltage_other = models.FloatField(null=True)


class SupplyAndDelivery(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    supply_total_kWh_from_IESO_dist_sys_of_host_distributor = models.FloatField()
    supply_total_kWh_from_embedded_generation_facilities = models.FloatField()
    amount_charged_by_host_distr_trans_low_voltage_services = models.FloatField()


class DemandAndRevenue(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    customer_or_connections = models.CharField(max_length=255)
    rate_class_generic = models.CharField(max_length=255)
    annual_billings_USoA_4080_dollars = models.FloatField()
    metered_consumption_in_kWh = models.FloatField()
    demand_in_kW = models.FloatField()


class UtilityCharacteristics(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    service_area_urban_square_kilometers = models.FloatField()
    service_area_rural_square_kilometers = models.FloatField()
    service_area_total_square_kilometers = models.FloatField()
    winter_peak_load_with_embedded_generation_kW = models.IntegerField()
    summer_peak_load_with_embedded_generation_kW = models.IntegerField()
    average_peak_load_with_embedded_generation_kW = models.IntegerField()
    average_load_factor_with_embedded_generation_percentage = models.FloatField()
    winter_peak_load_without_embedded_generation_kW = models.IntegerField()
    summer_peak_load_without_embedded_generation_kW = models.IntegerField()
    average_peak_load_without_embedded_generation_kW = models.FloatField()
    average_load_factor_without_embedded_generation_percentage = models.FloatField()
    primary_overhead_circuit_kilometers_of_line = models.FloatField(null=True)
    secondary_overhead_circuit_kilometers_of_line = models.FloatField(null=True)
    total_overhead_circuit_kilometers_of_line = models.FloatField()
    primary_underground_circuit_kilometers_of_line = models.FloatField(null=True)
    secondary_underground_circuit_kilometers_of_line = models.FloatField(null=True)
    total_underground_circuit_kilometers_of_line = models.FloatField()
    total_primary_circuit_kilometers_of_line = models.FloatField(null=True)
    total_secondary_circuit_kilometers_of_line = models.FloatField(null=True)
    total_circuit_kilometers_of_line = models.FloatField()


class RegulatedROE(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    regulated_net_income = models.FloatField()
    non_rate_regulated_items_and_other_adjustments = models.FloatField()
    unrealized_gains_on_interest_rate_swaps = models.FloatField(null=True)
    actuarial_gains_on_opeb_or_pensions_not_approved_by_the_oeb = models.FloatField()
    non_recoverable_donations = models.FloatField()
    net_interest_carrying_charges_from_dvas = models.FloatField()
    interest_adjustment_for_deemed_debt = models.FloatField()
    adjusted_regulated_net_income_before_tax_adjustments = models.FloatField()
    future_deferred_taxes_expense = models.FloatField()
    current_income_tax_expense = models.FloatField()
    current_income_tax_expense_for_regulated_roe_purpose = models.FloatField()
    adjusted_regulated_net_income = models.FloatField()
    working_capital_base = models.FloatField()
    working_capital_rate = models.FloatField()
    working_capital_allowance = models.FloatField()
    net_book_value_opening_balance = models.FloatField()
    net_book_value_adjusted_closing_balance = models.FloatField()
    net_book_value_average_balance = models.FloatField()
    total_rate_base = models.FloatField()
    cost_of_capital_short_term_debt = models.FloatField()
    cost_of_capital_long_term_debt = models.FloatField()
    cost_of_capital_common_equity = models.FloatField()
    short_term_debt = models.FloatField()
    long_term_debt = models.FloatField()
    common_equity = models.FloatField()
    achieved_roe = models.FloatField()
    deemed_income_from_cost_of_service = models.FloatField()
    deemed_equity_from_cost_of_service = models.FloatField()
    deemed_roe = models.FloatField()
    difference_achieved_roe_minus_deemed_roe = models.FloatField()
    roe_status = models.CharField(max_length=255)


class TrialBalanceBalanceSheet(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    cash_and_cash_equivalents = models.FloatField()
    receivables = models.FloatField()
    inventory = models.FloatField()
    inter_company_receivables = models.FloatField()
    other_current_assets = models.FloatField()
    current_assets_total = models.FloatField()
    property_plant_and_equipment = models.FloatField()
    accumulated_depreciation_and_amortization = models.FloatField()
    net_property_plant_and_equipment_total = models.FloatField()
    regulatory_assets = models.FloatField()
    inter_company_investments = models.FloatField()
    other_non_current_assets = models.FloatField()
    non_current_assets_total = models.FloatField()
    accounts_payable_and_accrued_charges = models.FloatField()
    other_current_liabilities = models.FloatField()
    inter_company_payables = models.FloatField()
    loans_notes_payable_and_current_portion_of_long_term_debt = models.FloatField()
    current_liabilities_total = models.FloatField()
    long_term_debt = models.FloatField()
    inter_company_long_term_debt_and_advances = models.FloatField()
    regulatory_liabilities = models.FloatField()
    other_deferred_amounts_and_customer_deposits = models.FloatField()
    employee_future_benefits = models.FloatField()
    deferred_taxes = models.FloatField()
    non_current_liabilities_total = models.FloatField()
    shareholders_equity = models.FloatField()


class TrialBalanceIncomeStatement(models.Model):
    company_name = models.CharField(max_length=255)
    year = models.IntegerField()
    power_revenue = models.FloatField()
    distribution_revenue = models.FloatField()
    cost_of_power_and_related_costs = models.FloatField()
    other_income_loss = models.FloatField()
    operating_expense = models.FloatField()
    maintenance_expense = models.FloatField()
    administrative_expense = models.FloatField()
    depreciation_and_amortization_expense = models.FloatField()
    financing_expense = models.FloatField()
    current_tax = models.FloatField()
    deferred_tax = models.FloatField()
    net_income_total = models.FloatField()
    other_comprehensive_income_loss = models.FloatField()
    comprehensive_income_loss_total = models.FloatField()
