
EumDateType = {
    Seconds : 0,
    Minutes : 1,
    Hours : 2,
    Days : 3,
    Months : 4,
    Years : 5
}


module.exports.Datetime = {

	/*EumDateType: function() {
		var TypeOfTime = {
		    Seconds : 0,
		    Minutes : 1,
		    Hours : 2,
		    Days : 3,
		    Months : 4,
		    Years : 5
		}
		return TypeOfTime;
	},*/

	IntToDate: function(num_date) {
		myDate = new Date(num_date);
		return myDate;
	},

	DateToInt: function(datetime) {
		numDate = datetime.getTime();
		return numDate;
	},

	/*	getFullYear()		Get the year (4 digits)
		getMonth() 			Get the month, from 0 to 11.
		getDate()			Get the day of month, from 1 to 31
		getHours()			Get hours of day, from 0 to 23
		getMinutes()		Get minutes of hour, from 0 to 59 
		getSeconds()		Get seconds of minute, from 0 to 59
		getMilliseconds()	Get milliseconds, from 0 to 999
	*/
	FormatString: function(datetime) {
		var str_datetime = datetime.getFullYear() + '-' + 
						(datetime.getMonth()+1) + '-' + 
						datetime.getDate() + ' ' +
						datetime.getHours() + ':' +
						datetime.getMinutes() + ':' +
						datetime.getSeconds();
		
		return str_datetime;
	},

	DateAdd: function(startDate, amount, typeOfDate) {
		var retDate;

		switch(typeOfDate) {
			case EumDateType.Seconds:
				retDate=new Date(
							startDate.getFullYear(),
							startDate.getMonth(),
							startDate.getDate(),
							startDate.getHours(),
							startDate.getMinutes(),
							startDate.getSeconds() + amount);
				break;
			case EumDateType.Minutes:
				retDate=new Date(
							startDate.getFullYear(),
							startDate.getMonth(),
							startDate.getDate(),
							startDate.getHours(),
							startDate.getMinutes() + amount,
							startDate.getSeconds());
				break;
			case EumDateType.Hours:
				retDate=new Date(
							startDate.getFullYear(),
							startDate.getMonth(),
							startDate.getDate(),
							startDate.getHours() + amount,
							startDate.getMinutes(),
							startDate.getSeconds());
				break;
			case EumDateType.Days:
				retDate=new Date(
							startDate.getFullYear(),
							startDate.getMonth(),
							startDate.getDate() + amount,
							startDate.getHours(),
							startDate.getMinutes(),
							startDate.getSeconds());
				break;
			case EumDateType.Months:
				retDate=new Date(
							startDate.getFullYear(),
							startDate.getMonth() + amount,
							startDate.getDate(),
							startDate.getHours(),
							startDate.getMinutes(),
							startDate.getSeconds());
				break;
			case EumDateType.Years:
				retDate=new Date(
							startDate.getFullYear() + amount,
							startDate.getMonth(),
							startDate.getDate(),
							startDate.getHours(),
							startDate.getMinutes(),
							startDate.getSeconds());
				break;
			default:
				retDate=new Date(
							startDate.getFullYear(),
							startDate.getMonth(),
							startDate.getDate(),
							startDate.getHours(),
							startDate.getMinutes(),
							startDate.getSeconds() + amount);
				break;
		}
		return retDate;
	}
}