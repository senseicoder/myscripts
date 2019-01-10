<?php
#https://www.twilio.com/blog/2017/03/google-spreadsheets-and-php.html
#passer sur https://developers.google.com/sheets/api/quickstart/php ?

require __DIR__ . '/../vendor/autoload.php';
use Google\Spreadsheet\DefaultServiceRequest;
use Google\Spreadsheet\ServiceRequestFactory;

class GDriveSpreadSheet
{
	function __construct($pathFileSecret)
	{
		putenv("GOOGLE_APPLICATION_CREDENTIALS=$pathFileSecret");
	}

	function GetSpreadSheetBase()
	{
		$client = new Google_Client;
		$client->useApplicationDefaultCredentials();
		 
		$client->setApplicationName("Something to do with my representatives");
		$client->setScopes(['https://www.googleapis.com/auth/drive','https://spreadsheets.google.com/feeds']);
		 
		if ($client->isAccessTokenExpired()) {
		    $client->refreshTokenWithAssertion();
		}
		 
		$accessToken = $client->fetchAccessTokenWithAssertion()["access_token"];

		$serviceRequest = new DefaultServiceRequest($accessToken);
		ServiceRequestFactory::setInstance($serviceRequest);

		// Get our spreadsheet
		$spreadsheetService = new Google\Spreadsheet\SpreadsheetService();
		return $spreadsheetService->getSpreadsheetFeed();
	}

	function GetSpreadSheet($sName)
	{
		$spreadsheetFeed = $this->GetSpreadSheetBase();
		$spreadsheet = $spreadsheetFeed->getByTitle($sName);

		if($spreadsheet === NULL) die(sprintf("fichier non trouvé ou non accessible (%s)\n", $sName));
		return $spreadsheet;
	}

	function GetSpreadSheetById($sId)
	{
		$spreadsheetFeed = $this->GetSpreadSheetBase();
		$spreadsheet = $spreadsheetFeed->getById($sId);

		if($spreadsheet === NULL) die(sprintf("fichier non trouvé ou non accessible (%s)\n", $sName));
		return $spreadsheet;
	}

	function GetWorkList($spreadsheet, $iNum)
	{
		// Get the first worksheet (tab)
		$worksheets = $spreadsheet->getWorksheets();
		$worksheet = $worksheets[$iNum];
		$listFeed = $worksheet->getListFeed();

		$aResult = array();
		foreach ($listFeed->getEntries() as $entry) {
			$aResult[] = $entry->getValues();
		}
		return $aResult;
	}
}
