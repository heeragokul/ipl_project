from django.views.generic import FormView, TemplateView, View
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.db.models import Count, Case, When

from matches.models import Matches, Deliveries
from matches.forms import SetIplSeasonForm



class HomeView(TemplateView):

    # template_name = 'matches/index.html'
    template_name = 'matches/examples.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        qs = Matches.objects.all().values('season').distinct()
        season_list =[year['season'] for year in qs]
        return {'season': season_list}


    def post(self, request, *args, **kwargs):
        context = {}
        # form = SetIplSeasonForm(request.POST)
        season = request.POST['season']
        top_4_teams = Matches.objects.filter(season=season).values('winner').annotate(num=Count('winner')).order_by('-num')[:4]
        max_toss_winner = Matches.objects.filter(season=season).values('toss_winner').annotate(num=Count('toss_winner')).order_by('-num')[0]
        max_player_of_match = Matches.objects.filter(season=season).values('player_of_match').annotate(num=Count('player_of_match')).order_by('-num')[0]
        max_winner_team = Matches.objects.filter(season=season).values('winner').annotate(num=Count('winner')).order_by('-num')[0]
        winner = max_winner_team['winner']
        max_wins_in_venue = Matches.objects.filter(season=season, winner=winner).values('venue').annotate(num=Count('venue')).order_by('-num')[0]
        total_toss_bat_count = Matches.objects.filter(season=season, toss_decision='bat').count()
        total_season_count = Matches.objects.filter(season=season).count()
        team_per_choose_batting = total_toss_bat_count/total_season_count * 100

        most_match_location = Matches.objects.filter(season=season).values('city').annotate(num=Count('city')).order_by('-num')[0]
        highest_margin_runs = Matches.objects.filter(season=season).values('winner', 'win_by_runs').order_by('-win_by_runs')[0]
        highest_wickets = Matches.objects.filter(season=season).values('winner', 'win_by_wickets').order_by('-win_by_wickets')[0]

        team_toss_win_qs = Matches.objects.filter(season=season).values('toss_winner', 'winner')
        team_toss_win_count = {}
        for i in team_toss_win_qs:
            if team_toss_win_count.get(i['toss_winner']) and i['toss_winner'] == i['winner']:
                team_toss_win_count[i['toss_winner']] = team_toss_win_count[i['toss_winner']] + 1
            elif i['toss_winner'] == i['winner']:
                team_toss_win_count[i['toss_winner']] = 1
            elif not team_toss_win_count.get(i['toss_winner']):
                team_toss_win_count[i['toss_winner']] = 0
        max_run_by_batsman  = Deliveries.objects.filter(match_id__season=season).values('batsman').annotate(num=Count('total_runs')).order_by('-num')[0]
        total_num_catches = Deliveries.objects.filter(match_id__season=season, dismissal_kind='caught').values('fielder').annotate(num=Count('fielder')).order_by('-num')[0]
        qs = Matches.objects.all().values('season').distinct()
        season_list = [year['season'] for year in qs]
        context['result'] = True
        context['top_4_teams'] = top_4_teams
        context['max_toss_winner'] = max_toss_winner
        context['max_player_of_match'] = max_player_of_match
        context['max_winner_team'] = max_winner_team
        context['max_wins_in_venue'] = max_wins_in_venue
        context['bat_choose_percentage'] = {'total_toss_bat_count': total_toss_bat_count,
                                            'total_season_count': total_season_count,
                                            'team_per_choose_batting': team_per_choose_batting}
        context['most_match_location'] = most_match_location
        context['highest_margin_runs'] = highest_margin_runs
        context['highest_wickets'] = highest_wickets
        context['team_toss_win_count'] = team_toss_win_count
        context['max_run_by_batsman'] = max_run_by_batsman
        context['total_num_catches'] = total_num_catches
        context['season'] = season_list
        return render(request, self.template_name, context)
