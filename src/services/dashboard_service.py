from src.services.ad_service import get_ad_model
from src.services.booking_service import get_bookings_model
from src.services.calander_service import get_calendar_model
from src.services.goal_service import get_dash_model


def get_dashboard_data(user_id):
   
   dashboard_data = {
      "dash_ad" : None,
      "dash_bookings": None,
      "dash_calender" : None,
      "dash_goals" : None
   }

   dashboard_data["dash_ad"] =  get_ad_model(user_id)
   dashboard_data["dash_bookings"] = get_bookings_model(user_id)
   dashboard_data["dash_calender"] = get_calendar_model(user_id)
   dashboard_data["dash_goals"] = get_dash_model(user_id)

   return dashboard_data


    