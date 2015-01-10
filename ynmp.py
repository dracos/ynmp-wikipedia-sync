import urllib
import json
import logging
from shared import Candidate

def all_constituencies():
	req = urllib.urlopen("http://mapit.mysociety.org/areas/WMC")
	page = req.read()
	data = json.loads(page)
	for constituency_data in data.values():
		yield constituency_data["id"], constituency_data["name"]

def fetch_candidates_in_constituency(constituency_id):
	logging.debug("candidates_in_constituency(%r)", constituency_id)
	req = urllib.urlopen("http://yournextmp.popit.mysociety.org/api/v0.1/posts/%d?embed=membership.person" % (constituency_id,))
	page = req.read()
	data = json.loads(page)
	return data

def candidates_in_constituency(constituency_id):
	data = fetch_candidates_in_constituency(constituency_id)
	for person in data["result"]["memberships"]:
		try:
			# logging.debug("candidate: %r %r %r" % (person["person_id"]["name"], person["person_id"]["party_memberships"], person["person_id"]["standing_in"],))
			if "2015" in person["person_id"]["standing_in"]:
				yield Candidate(
					person_id=person["person_id"]["id"],
					name=person["person_id"]["name"],
					party_id=person["person_id"]["party_memberships"]["2015"]["id"],
					party=person["person_id"]["party_memberships"]["2015"]["name"])
		except Exception:
			logging.exception("Unable to parse %r", person)
			raise

if __name__ == '__main__':
	with open("candidates_from_ynmp.json", "w") as f:
		json.dump({
			"%s:%s" % (constituency_id, constituency_name,) : list(candidates_in_constituency(constituency_id))
			for constituency_id, constituency_name in all_constituencies()}, f)
